from fastapi import APIRouter, Depends, UploadFile, File

from app.models import User
from app.api.dependencies import get_current_user
from app.utils.storage import save_uploaded_file

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    save_uploaded_file(file)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }