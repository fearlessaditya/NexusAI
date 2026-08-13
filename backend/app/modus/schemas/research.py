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
    evidence: list[ResearchEvidence]
    comparison: ResearchComparison
    conclusion: ResearchConclusion

class ResearchEvidence(BaseModel):
    claim: str
    evidence: str
    source_index: int
    source: ResearchSource

class Contradiction(BaseModel):
    claim_a: str
    claim_b: str
    explanation: str
    source_a: int
    source_b: int


class ResearchComparison(BaseModel):
    agreements: list[str]
    disagreements: list[str]
    contradictions: list[Contradiction]

class ResearchConclusion(BaseModel):
    conclusion: str
    confidence: str
    key_takeaways: list[str]
    caveats: list[str]