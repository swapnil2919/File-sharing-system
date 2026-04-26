import os
import uuid

async def save_file(file, upload_dir):
    os.makedirs(upload_dir, exist_ok=True)

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(upload_dir, unique_name)

    with open(path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    return path, unique_name