import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.file import router
from app.core.logging import logger
from app.workers.cleanup import cleanup_files

# Create FastAPI app
app = FastAPI()

# ✅ CORS Middleware (ADD HERE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


# Logging Middleware
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response

# Background cleanup task
@app.on_event("startup")
async def start_cleanup():

    async def run():
        while True:
            await cleanup_files()
            await asyncio.sleep(3600)  # every 1 hour

    asyncio.create_task(run())