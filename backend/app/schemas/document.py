from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    uploaded_by: str

    class Config:
        from_attributes = True