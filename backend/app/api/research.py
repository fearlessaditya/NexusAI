from fastapi import APIRouter

from app.modus.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)

from app.modus.research.research_service import (
    run_research,
)


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post(
    "/run",
    response_model=ResearchResponse,
)
def research(request: ResearchRequest):

    return run_research(
        question=request.question,
        top_k=request.top_k,
    )