from datetime import datetime

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from zoneinfo import ZoneInfo

from src.pi_cloud.models import FileUpload
from src.pi_cloud.worker import store_file

app = FastAPI()

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


@app.post("/file/upload")
def upload_file(file: UploadFile):
    # https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile

    # Create FileUpload instance with file paramater
    file_upload = FileUpload(
        name=file.filename,
        size=file.size,
        content=file.file.read(),
        upload_time=datetime.now().astimezone(ZoneInfo("UTC")),
    )

    # Write file to disk
    store_file(file_upload)
    return file_upload.model_dump()
