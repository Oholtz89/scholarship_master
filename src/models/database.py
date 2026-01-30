"""SQLAlchemy database models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SubmissionORM(Base):
    """ORM model for submissions."""
    
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    applicant_name = Column(String, index=True)
    applicant_email = Column(String, index=True)
    submission_folder_id = Column(String, unique=True, index=True)
    status = Column(String, default="pending")  # pending, processing, completed, error
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    error_message = Column(Text, nullable=True)
    
    documents = relationship("DocumentORM", back_populates="submission", cascade="all, delete-orphan")
    scores = relationship("ScoreORM", back_populates="submission", cascade="all, delete-orphan")


class DocumentORM(Base):
    """ORM model for documents."""
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), index=True)
    name = Column(String)
    google_drive_id = Column(String, unique=True, index=True)
    mime_type = Column(String)
    category = Column(String, nullable=True, index=True)
    downloaded_path = Column(String, nullable=True)
    file_size = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    
    submission = relationship("SubmissionORM", back_populates="documents")
    scores = relationship("ScoreORM", back_populates="document", cascade="all, delete-orphan")


class ScoreORM(Base):
    """ORM model for document scores."""
    
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), index=True)
    category = Column(String, index=True)
    total_score = Column(Float)
    max_score = Column(Float, default=100.0)
    criteria_scores = Column(JSON, default={})
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("DocumentORM", back_populates="scores")
    submission = relationship("SubmissionORM", back_populates="scores")
