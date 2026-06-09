import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.constants import UPLOAD_DIR


def save_uploaded_file(file: UploadFile) -> Path:

    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path