from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.db.session import SessionLocal
from app.models.file import File as FileModel
from app.models.download import Download
from app.services.file_service import create_file_record
from app.utils.storage import save_file
from app.core.config import ALLOWED_TYPES, MAX_FILE_SIZE

router = APIRouter()


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    days: int = None,
    one_time: bool = False,
    db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")

    path, stored_name = await save_file(file, "uploads")

    db_file = await create_file_record(
        db, file, path, stored_name, days, one_time
    )

    return {
        "file_hash": db_file.file_hash,
        "download_url": f"/download/{db_file.file_hash}"
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
        raise HTTPException(410, "File expired")

    if file.is_one_time and file.download_count >= 1:
        if not file.deleted_at:
            file.deleted_at = datetime.utcnow()
            await db.commit()
        raise HTTPException(404, not_available_message)

    # Track download
    download = Download(
        file_id=file.id,
        downloader_ip=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    db.add(download)

    file.download_count += 1

    if file.is_one_time:
        file.deleted_at = datetime.utcnow()

    await db.commit()

    return FileResponse(file.file_path, filename=file.original_filename)
