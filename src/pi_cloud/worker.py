import pickle
from pathlib import Path

from fastapi import FastAPI

from src.pi_cloud.models import FileMetadata, FileUpload

UPLOADS_DIR = Path("uploads")


class Worker:
    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app
        self.stored_files: dict[str, FileMetadata] = Worker._read_file_metadata()

    @staticmethod
    def _read_file_metadata() -> dict[str, FileMetadata]:
        with Path.open("file_metadata.db", "rb") as file:
            return pickle.load(file)  # noqa: S301

    def get_file(self, file_id: str) -> bytes:
        with Path.open(f"{UPLOADS_DIR.name}/{file_id}", "rb") as f:
            return f.read()

    def store_file(self, file: FileUpload) -> str:
        """
        Store file in 'uploads' directory with its uuid as the filename
        """
        with Path.open(f"{UPLOADS_DIR.name}/{file.file_id}", "wb") as f:
            f.write(file.content)
        self.stored_files[file.file_id] = FileMetadata(
            name=file.name,
            size=file.size,
            file_id=file.file_id,
            upload_time=file.upload_time.isoformat(),
            tags=file.tags,
        )
        self.write_file_metadata()
        return file.file_id

    def write_file_metadata(self) -> None:
        with Path.open("file_metadata.db", "wb") as file:
            pickle.dump(self.stored_files, file)

    def get_stored_files_preview(self) -> list[dict[str, str]]:
        preview = []
        for file_metadata in self.stored_files.values():
            preview.append(file_metadata.model_dump(include={"name", "upload_time", "file_id"}))  # noqa: PERF401
        return preview
