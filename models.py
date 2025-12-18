from sqlalchemy import Column, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    title = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID, ForeignKey("conversations.id"))
    role = Column(Text)
    content = Column(Text)

    extra_data = Column("metadata", JSONB)  # ✅ renommé côté Python

    created_at = Column(TIMESTAMP, server_default=func.now())

class GeneratedFile(Base):
    __tablename__ = "generated_files"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID, ForeignKey("conversations.id"))
    file_name = Column(Text)
    file_type = Column(Text)
    file_path = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
