from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from src.pi_cloud.models import FileMetadata, FileUpload
from src.pi_cloud.worker import Worker

app = FastAPI()
worker = Worker(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/files")
def list_files() -> list[dict[str, str]]:
    return worker.get_stored_files_preview()


@app.get("/file/{file_id}")
def get_file(file_id: str) -> FileResponse:
    return worker.get_file(file_id)


@app.delete("/file/{file_id}")
def delete_file(file_id: str) -> dict[str, str]:
    worker.delete_file(file_id)
    return {"message": "File deleted"}


@app.get("/file/{file_id}/metadata")
def get_file_metadata(file_id: str) -> dict[str, str | int | list]:
    return worker.stored_files[file_id].model_dump()


@app.post("/file/upload")
def upload_file(file: UploadFile) -> FileMetadata:
    # https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile
    print("Starting file upload")
    # Create FileUpload instance with file paramater
    file_upload = FileUpload(
        name=file.filename,
        size=file.size,
        content=file.file.read(),
    )
    print("FileUpload instance created")
    # Write file to disk
    metadata: FileMetadata = worker.store_file(file_upload)
    return metadata
