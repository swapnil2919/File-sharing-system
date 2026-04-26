# Spider Sharing

Spider Sharing is a simple file-sharing application with a React frontend and a FastAPI backend. It lets users upload files, generate a shareable hash-based link, and download files later. It also supports one-time download links and file expiry.

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

3. Create a `.env` file with at least:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
UPLOAD_DIR=uploads
```

4. Start the backend server:

```bash
uvicorn app.main:app --reload
```

Run this command from the `backend` folder.

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

The frontend is configured to call the backend at `http://localhost:8000`.

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
- One-time files become unavailable after the first successful download
- Expired or missing hashes return a "No such file available on server" style error for handled cases on the frontend
