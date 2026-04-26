from datetime import datetime, timedelta
from app.models.file import File
from app.utils.security import generate_hash

async def create_file_record(db, file, path, stored_name, days, one_time):

    if days and days > 7:
        raise ValueError("Max 7 days allowed")

    expires_at = None
    if days:
        expires_at = datetime.utcnow() + timedelta(days=days)

    file_hash = generate_hash()

    db_file = File(
        original_filename=file.filename,
        stored_filename=stored_name,
        file_size=file.size,
        file_type=file.content_type,
        file_path=path,
        file_hash=file_hash,
        expires_at=expires_at,
        is_one_time=one_time
    )

    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)

    return db_file