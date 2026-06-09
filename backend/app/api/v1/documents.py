from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import HTTPException
from app.models import User
from app.api.dependencies import get_current_user
from app.utils.storage import save_uploaded_file
from app.utils.file_utils import get_file_type
from app.services.extractors.selector import TextExtractorSelector

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:

        file_type = get_file_type(file.filename)

        file_path = save_uploaded_file(file)

        extractor = TextExtractorSelector()

        text = extractor.extract(
            file_type=file_type,
            file_path=str(file_path)
        )

        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "text_preview": text[:500]
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    