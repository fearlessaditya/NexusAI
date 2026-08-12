from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(default=5, ge=1, le=10)


class ResearchSource(BaseModel):
    document: str
    metadata: dict
    hybrid_score: float | None = None


class ResearchFinding(BaseModel):
    claim: str
    evidence: str
    source_index: int


class ResearchAnalysis(BaseModel):
    summary: str
    findings: list[ResearchFinding]
    limitations: list[str]


class ResearchResponse(BaseModel):
    question: str
    answer: str
    findings: ResearchAnalysis
    sources: list[ResearchSource]