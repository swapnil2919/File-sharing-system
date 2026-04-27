# Spider Sharing

Spider Sharing is a file-sharing application with a React frontend and a FastAPI backend. Users can upload a file, get a shareable hash-based link, and download it later with optional one-time access or expiry.

## Features

- Upload files and generate a unique download hash
- Download files using the shared hash
- Optional one-time download support
- Optional file expiry support
- Simple branded frontend UI

## Tech Stack

- Frontend: React + Vite + Axios
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL via `asyncpg`

## Project Structure

```text
backend/
  app/
    api/
    core/
    db/
    models/
    services/
    utils/
    workers/
frontend/
  src/
README.md
```

## Backend Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Create a `backend/.env` file with:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_STORAGE_BUCKET=shared-files
FRONTEND_ORIGIN=http://localhost:5173
```

4. Start the backend server:

```bash
uvicorn app.main:app --reload
```

Run this command from the `backend` folder.

## Production Storage Model

This project is now designed for production file storage in `Supabase Storage`, not a local `uploads/` folder.

- Uploaded files are stored in a private Supabase bucket.
- File metadata and expiry settings remain in the database.
- The backend validates download access before returning the file.
- One-time files are deleted from storage after the first successful download.
- Expired files are removed by the cleanup worker so storage space is released.

For Render deployment, set the same backend environment variables in the Render dashboard. For the frontend on Vercel, set:

```env
VITE_API_BASE_URL=https://your-render-service-url.onrender.com
```

## Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start the frontend:

```bash
npm run dev
```

The frontend reads the backend URL from `VITE_API_BASE_URL` and falls back to `http://localhost:8000` for local development.

## Allowed Upload Types

The backend currently allows:

- PNG
- JPEG
- PDF
- ZIP
- Python files
- Plain text files

## Notes

- Maximum file size is currently `50 MB`
- File expiry is capped at `7 days`
- One-time files become unavailable after the first successful download and are deleted from storage
- Expired files are blocked immediately and removed from storage by the cleanup worker
