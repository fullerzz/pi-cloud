from pathlib import Path

from src.pi_cloud.models import FileUpload


def store_file(file: FileUpload):
    """
    Store file in a directory
    """
    with Path.open(f"uploads/{file.name}", "wb") as f:
        f.write(file.content)
    return {"message": "File stored successfully"}
