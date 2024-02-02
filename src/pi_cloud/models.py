from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field
from zoneinfo import ZoneInfo


class FileUpload(BaseModel):
    """
    Object built from user's file upload
    """

    name: str
    size: int
    content: bytes
    file_id: str = Field(default_factory=lambda: uuid4().hex)
    upload_time: datetime = Field(
        default_factory=lambda: datetime.now().astimezone(ZoneInfo("UTC"))
    )
    tags: list[str] = []


class FileMetadata(BaseModel):
    name: str
    size: int
    file_id: str
    upload_time: str
    tags: list[str]
