import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

ALLOWED_TYPES = [
    "image/png",
    "image/jpeg",
    "application/pdf",
    "application/zip",        # .zip files
    "application/x-zip-compressed",  # some systems use this
    "text/x-python",          # .py files
    "text/plain"              # fallback for .py (sometimes detected as plain text)
]