import os
from datetime import datetime
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.file import File

async def cleanup_files():

    async with SessionLocal() as db:

        result = await db.execute(
            select(File).where(
                (File.expires_at < datetime.utcnow()) |
                (File.deleted_at != None)
            )
        )

        files = result.scalars().all()

        for file in files:
            try:
                if os.path.exists(file.file_path):
                    os.remove(file.file_path)
            except:
                pass

        await db.commit()