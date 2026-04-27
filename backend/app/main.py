import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.file import router
from app.core.config import FRONTEND_ORIGIN
from app.core.logging import logger
from app.workers.cleanup import cleanup_files

app = FastAPI()

allowed_origins = ["*"] if FRONTEND_ORIGIN == "*" else [FRONTEND_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response


@app.on_event("startup")
async def start_cleanup():
    async def run():
        while True:
            await cleanup_files()
            await asyncio.sleep(3600)

    asyncio.create_task(run())
