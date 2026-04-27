from datetime import datetime
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.file import File
from app.utils.storage import StorageError, delete_files

async def cleanup_files():

    async with SessionLocal() as db:

        result = await db.execute(
            select(File).where(
                (File.expires_at < datetime.utcnow()) |
                (File.deleted_at != None)
            )
        )

        files = result.scalars().all()
        object_paths = [file.file_path for file in files if file.file_path]

        if object_paths:
            try:
                await delete_files(object_paths)
            except StorageError:
                pass

        for file in files:
            if not file.deleted_at:
                file.deleted_at = datetime.utcnow()

        await db.commit()
