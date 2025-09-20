import os
import uuid
import base64
import contextlib
from typing import AsyncGenerator
from aiohttp.streams import StreamReader
from azure.storage.blob.aio import BlobServiceClient
from azure.identity.aio import DefaultAzureCredential
from pathlib import Path


SUSTINEO_STORAGE = os.environ.get("SUSTINEO_STORAGE", "EMPTY")
# When SUSTINEO_STORAGE is unset or 'EMPTY', fall back to local filesystem
local_storage = not SUSTINEO_STORAGE or SUSTINEO_STORAGE.upper() == "EMPTY"
SUSTINEO_CONTAINER = "sustineo"

# Local public directories (served by API endpoints)
REPO_ROOT = Path(__file__).resolve().parents[1]
public_web_dir = REPO_ROOT / "web" / "public"
public_images_dir = public_web_dir / "images"
public_videos_dir = public_web_dir / "videos"
public_images_dir.mkdir(parents=True, exist_ok=True)
public_videos_dir.mkdir(parents=True, exist_ok=True)


@contextlib.asynccontextmanager
async def get_storage_client(container: str):
    # Create credential and blob service client
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(
        account_url=SUSTINEO_STORAGE, credential=credential
    )
    try:
        # Create the container if it doesn't exist
        container_client = blob_service_client.get_container_client(container)

        # remove the comment below if you want to ensure
        # the container exists. commenting to avoid unnecessary
        # creation
        # if not await container_client.exists():
        #    await container_client.create_container()

        yield container_client
    finally:
        await credential.close()
        await blob_service_client.close()


async def save_image_blobs(
    images: list[str], path: str | None = None
) -> AsyncGenerator[str, None]:
    # Local filesystem fallback
    if local_storage:
        for image in images:
            image_bytes = base64.b64decode(image)
            filename = f"{str(uuid.uuid4())}.png"
            if path is None:
                dest = public_images_dir / filename
                blob_name = f"images/{filename}"
            else:
                subdir = public_images_dir / path
                subdir.mkdir(parents=True, exist_ok=True)
                dest = subdir / filename
                blob_name = f"images/{path}/{filename}"

            with open(dest, "wb") as f:
                f.write(image_bytes)

            yield blob_name

        return

    # Azure Blob Storage path
    async with get_storage_client(SUSTINEO_CONTAINER) as container_client:
        for image in images:
            image_bytes = base64.b64decode(image)
            blob_name = (
                f"images/{str(uuid.uuid4())}.png"
                if path is None
                else f"images/{path}/{str(uuid.uuid4())}.png"
            )
            await container_client.upload_blob(
                name=blob_name, data=image_bytes, overwrite=True
            )
            yield blob_name


async def save_image_blob(image: str, path: str | None = None) -> str:
    if local_storage:
        image_bytes = base64.b64decode(image)
        filename = f"{str(uuid.uuid4())}.png"
        if path is None:
            dest = public_images_dir / filename
            blob_name = f"images/{filename}"
        else:
            subdir = public_images_dir / path
            subdir.mkdir(parents=True, exist_ok=True)
            dest = subdir / filename
            blob_name = f"images/{path}/{filename}"

        with open(dest, "wb") as f:
            f.write(image_bytes)

        return blob_name

    async with get_storage_client(SUSTINEO_CONTAINER) as container_client:
        image_bytes = base64.b64decode(image)
        blob_name = (
            f"images/{str(uuid.uuid4())}.png"
            if path is None
            else f"images/{path}/{str(uuid.uuid4())}.png"
        )
        await container_client.upload_blob(name=blob_name, data=image_bytes, overwrite=True)
        return blob_name


async def save_video_blob(stream_reader: StreamReader, path: str | None = None) -> str:
    if local_storage:
        blob_name = (
            f"videos/{str(uuid.uuid4())}.mp4"
            if path is None
            else f"videos/{path}/{str(uuid.uuid4())}.mp4"
        )
        filename = blob_name.split("/", 1)[1]
        dest = public_videos_dir / filename if path is None else (public_videos_dir / path / filename)
        dest.parent.mkdir(parents=True, exist_ok=True)
        content = await stream_reader.read()
        with open(dest, "wb") as f:
            f.write(content)
        return blob_name

    async with get_storage_client(SUSTINEO_CONTAINER) as container_client:
        blob_name = (
            f"videos/{str(uuid.uuid4())}.mp4"
            if path is None
            else f"videos/{path}/{str(uuid.uuid4())}.mp4"
        )
        content = await stream_reader.read()
        await container_client.upload_blob(name=blob_name, data=content, overwrite=True)
        return blob_name
