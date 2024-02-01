from datetime import datetime

from pydantic import BaseModel


class FileUpload(BaseModel):
    """
    Object built from user's file upload
    """

    name: str
    size: int
    content: bytes
    upload_time: datetime
    tags: list[str] = []
