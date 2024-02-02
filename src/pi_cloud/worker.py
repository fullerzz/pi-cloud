import json
import pickle
from pathlib import Path

from fastapi import FastAPI

from src.pi_cloud.models import FileMetadata, FileUpload

UPLOADS_DIR = Path("uploads")


class Worker:
    def __init__(self, app: FastAPI) -> None:
        self.app: FastAPI = app
        self.stored_files: dict[str, FileMetadata] = {}
        self._read_file_metadata()
        print(self.stored_files)

    def _read_file_metadata(self) -> dict[str, FileMetadata]:
        try:
            file_metadata: dict = {}
            with Path.open("file_metadata.json", "r") as file:
                file_metadata = json.load(file)
                # return pickle.load(file)
            for file_id, metadata in file_metadata.items():
                self.stored_files[file_id] = FileMetadata(**metadata)
        except Exception:
            return {}

    def get_file(self, file_id: str) -> bytes:
        with Path.open(f"{UPLOADS_DIR.name}/{file_id}", "rb") as f:
            return f.read()

    def store_file(self, file: FileUpload) -> FileMetadata:
        """
        Store file in 'uploads' directory with its uuid as the filename
        """
        with Path.open(f"{UPLOADS_DIR.name}/{file.file_id}", "wb") as f:
            f.write(file.content)
        print("Wrote file to disk")
        metadata = FileMetadata(
            name=file.name,
            size=file.size,
            file_id=file.file_id,
            upload_time=file.upload_time.isoformat(),
            tags=file.tags,
        )
        self.stored_files[file.file_id] = metadata
        self.write_file_metadata()
        return metadata

    def write_file_metadata(self) -> None:
        file_metadata: dict = {}
        print(self.stored_files)
        for file_id, metadata in self.stored_files.items():
            file_metadata[file_id] = metadata.model_dump()
        print(json.dumps(file_metadata, indent=4))
        with Path.open("file_metadata.json", "w") as file:
            json.dump(file_metadata, file)
            # pickle.dump(self.stored_files, file)
        print("yuh")

    def get_stored_files_preview(self) -> list[dict[str, str]]:
        preview = []
        for file_metadata in self.stored_files.values():
            preview.append(file_metadata.model_dump(include={"name", "upload_time", "file_id"}))  # noqa: PERF401
        return preview
