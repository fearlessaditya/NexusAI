from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    filename: str,
    filepath: str,
    uploaded_by: str,
) -> Document:

    document = Document(
        filename=filename,
        filepath=filepath,
        uploaded_by=uploaded_by,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document