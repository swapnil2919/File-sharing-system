from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.file import File as FileModel
from app.models.download import Download
from app.services.file_service import create_file_record
from app.utils.storage import StorageError, delete_files, download_file as download_from_storage, save_file
from app.core.config import ALLOWED_TYPES, MAX_FILE_SIZE

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    days: int = None,
    one_time: bool = False,
    db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    uploaded_size = getattr(file, "size", None)
    if uploaded_size and uploaded_size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")

    try:
        path, stored_name, file_size = await save_file(file)
    except StorageError as exc:
        raise HTTPException(500, str(exc)) from exc

    db_file = await create_file_record(
        db, file, path, stored_name, days, one_time, file_size
    )

    return {
        "file_hash": db_file.file_hash,
        "download_url": str(request.url_for("download_file", file_hash=db_file.file_hash))
    }


@router.get("/download/{file_hash}")
async def download_file(
    file_hash: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    not_available_message = "No such file available on server"

    result = await db.execute(
        select(FileModel).where(FileModel.file_hash == file_hash)
    )
    file = result.scalar_one_or_none()

    if not file or file.deleted_at:
        raise HTTPException(404, not_available_message)

    if file.expires_at and datetime.utcnow() > file.expires_at:
        if not file.deleted_at:
            file.deleted_at = datetime.utcnow()
            await db.commit()
        try:
            await delete_files([file.file_path])
        except StorageError:
            pass
        raise HTTPException(410, "File expired")

    if file.is_one_time and file.download_count >= 1:
        if not file.deleted_at:
            file.deleted_at = datetime.utcnow()
            await db.commit()
        try:
            await delete_files([file.file_path])
        except StorageError:
            pass
        raise HTTPException(404, not_available_message)

    try:
        file_bytes = await download_from_storage(file.file_path)
    except StorageError as exc:
        raise HTTPException(502, str(exc)) from exc

    if file_bytes is None:
        if not file.deleted_at:
            file.deleted_at = datetime.utcnow()
            await db.commit()
        raise HTTPException(404, not_available_message)

    download = Download(
        file_id=file.id,
        downloader_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    db.add(download)

    file.download_count += 1

    if file.is_one_time:
        file.deleted_at = datetime.utcnow()

    await db.commit()

    if file.is_one_time:
        try:
            await delete_files([file.file_path])
        except StorageError:
            pass

    return Response(
        content=file_bytes,
        media_type=file.file_type or "application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{file.original_filename}"'
        },
    )
