import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.services.document_service import create_document
from app.utils.security import admin_required

from app.services.parser_service import (
    extract_pdf_text,
    extract_docx_text,
)

from app.services.langchain_chunk_service import (
    chunk_text_langchain,
)

from app.services.embedding_service import (
    create_embeddings,
)

from app.services.vector_service import (
    store_embeddings,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_FOLDER = "uploads"


@router.post(
    "/upload",
    response_model=DocumentResponse,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):

    # Allow only PDF and DOCX
    allowed_extensions = [".pdf", ".docx"]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed",
        )

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    if extension == ".pdf":
        text = extract_pdf_text(file_path)
    else:
        text = extract_docx_text(file_path)

# Create chunks
    chunks = chunk_text_langchain(text)

# Generate embeddings
    embeddings = create_embeddings(chunks)

# Store in ChromaDB
    # Store in ChromaDB
    store_embeddings(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename,
        uploaded_by=current_user.email,
)

    document = create_document(
        db=db,
        filename=file.filename,
        filepath=file_path,
        uploaded_by=current_user.email,
    )

    return document