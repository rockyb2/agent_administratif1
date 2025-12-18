from models import Message, GeneratedFile
from sqlalchemy.orm import Session

def save_message(db: Session, conversation_id, role, content, metadata=None):
    msg = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        metadata=metadata
    )
    db.add(msg)
    db.commit()

def save_generated_file(db: Session, conversation_id, file_path):
    file_name = file_path.split("/")[-1]
    file_type = file_name.split(".")[-1]

    f = GeneratedFile(
        conversation_id=conversation_id,
        file_name=file_name,
        file_type=file_type,
        file_path=file_path
    )
    db.add(f)
    db.commit()
