from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.literature_review_service import LiteratureReviewService

router = APIRouter()
service = LiteratureReviewService()

class GenerateLiteratureReviewRequest(BaseModel):
    writing_id: str
    section_id: str
    title: str
    paper_title: str
    organization_method: str

class GenerateLiteratureReviewResponse(BaseModel):
    researchStatus: str
    researchGaps: str
    literatureEvaluation: str

@router.post("/generate", response_model=GenerateLiteratureReviewResponse)
async def generate_literature_review(request: GenerateLiteratureReviewRequest):
    try:
        return await service.generate_literature_review(
            writing_id=request.writing_id,
            section_id=request.section_id,
            title=request.title,
            organization_method=request.organization_method
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 