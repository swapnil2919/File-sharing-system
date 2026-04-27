import uuid
from urllib.parse import quote

import httpx

from app.core.config import SUPABASE_SERVICE_ROLE_KEY, SUPABASE_STORAGE_BUCKET, SUPABASE_URL


class StorageError(Exception):
    pass


_bucket_ready = False


def _ensure_storage_config():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise StorageError(
            "Supabase storage is not configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY."
        )


def _storage_headers(content_type=None):
    headers = {
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def _object_url(object_path, authenticated=True):
    encoded_path = quote(object_path, safe="/")
    route = "authenticated" if authenticated else ""
    route_prefix = f"/{route}" if route else ""
    return (
        f"{SUPABASE_URL}/storage/v1/object{route_prefix}/"
        f"{SUPABASE_STORAGE_BUCKET}/{encoded_path}"
    )


async def _ensure_bucket_exists(client):
    global _bucket_ready

    if _bucket_ready:
        return

    response = await client.get(
        f"{SUPABASE_URL}/storage/v1/bucket/{SUPABASE_STORAGE_BUCKET}",
        headers=_storage_headers(),
    )
    if response.status_code == 200:
        _bucket_ready = True
        return

    if response.status_code == 404:
        create_response = await client.post(
            f"{SUPABASE_URL}/storage/v1/bucket",
            headers=_storage_headers("application/json"),
            json={
                "id": SUPABASE_STORAGE_BUCKET,
                "name": SUPABASE_STORAGE_BUCKET,
                "public": False,
            },
        )
        if create_response.status_code >= 400:
            raise StorageError(create_response.text or "Failed to create storage bucket")
        _bucket_ready = True
        return

    raise StorageError(response.text or "Failed to check storage bucket")


async def save_file(file):
    _ensure_storage_config()
    content = await file.read()
    stored_name = f"{uuid.uuid4()}_{file.filename}"
    object_path = f"shared/{stored_name}"
    content_type = file.content_type or "application/octet-stream"

    async with httpx.AsyncClient(timeout=60.0) as client:
        await _ensure_bucket_exists(client)
        response = await client.post(
            _object_url(object_path, authenticated=False),
            headers=_storage_headers(content_type),
            content=content,
        )

    if response.status_code >= 400:
        raise StorageError(response.text or "Failed to upload file to storage")

    return object_path, stored_name, len(content)


async def download_file(object_path):
    _ensure_storage_config()

    async with httpx.AsyncClient(timeout=60.0) as client:
        await _ensure_bucket_exists(client)
        response = await client.get(
            _object_url(object_path, authenticated=True),
            headers=_storage_headers(),
        )

    if response.status_code == 404:
        return None

    if response.status_code >= 400:
        raise StorageError(response.text or "Failed to download file from storage")

    return response.content


async def delete_files(object_paths):
    if not object_paths:
        return

    _ensure_storage_config()

    async with httpx.AsyncClient(timeout=60.0) as client:
        await _ensure_bucket_exists(client)
        response = await client.request(
            "DELETE",
            f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_STORAGE_BUCKET}",
            headers=_storage_headers("application/json"),
            json={"prefixes": object_paths},
        )

    if response.status_code >= 400:
        raise StorageError(response.text or "Failed to delete files from storage")
