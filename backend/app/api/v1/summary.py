from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
    get_db,
    get_summary_service
)
from app.models import User
from app.schemas.summary import SummaryResponse
from app.services.summary.summary_service import SummaryService


router = APIRouter(
    prefix="/documents",
    tags=["Summary"]
)


@router.post("/{document_id}/summary",response_model=SummaryResponse)
def summarize_document(document_id: UUID,current_user: User = Depends(get_current_user),db: Session = Depends(get_db),summary_service: SummaryService = Depends(get_summary_service)):
    try:
        response = summary_service.summarize(
            document_id=document_id,
            owner_id=current_user.id,
            department=current_user.department.value,
            db=db
        )
        return SummaryResponse(**response)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc)
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc)
        )