import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "file-sharing")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")
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
