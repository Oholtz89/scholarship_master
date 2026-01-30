"""Pydantic schemas for data validation."""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class DocumentBase(BaseModel):
    """Base document model."""
    
    name: str
    google_drive_id: str
    mime_type: str
    category: Optional[str] = None


class Document(DocumentBase):
    """Document model with metadata."""
    
    id: Optional[int] = None
    submission_id: int
    downloaded_path: Optional[str] = None
    file_size: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = False
    error_message: Optional[str] = None


class ScoreBase(BaseModel):
    """Base score model."""
    
    category: str
    total_score: float
    max_score: float = 100.0
    criteria_scores: Dict[str, float] = {}


class Score(ScoreBase):
    """Score model with metadata."""
    
    id: Optional[int] = None
    document_id: int
    feedback: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SubmissionBase(BaseModel):
    """Base submission model."""
    
    applicant_name: str
    applicant_email: str
    submission_folder_id: str


class Submission(SubmissionBase):
    """Submission model with documents and scores."""
    
    id: Optional[int] = None
    documents: Optional[list[Document]] = []
    scores: Optional[list[Score]] = []
    status: str = "pending"  # pending, processing, completed, error
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None


class GradingRequest(BaseModel):
    """Request to grade a document."""
    
    document_id: int
    category: str
    content: str


class GradingResult(BaseModel):
    """Result of grading a document."""
    
    document_id: int
    category: str
    total_score: float
    max_score: float
    criteria_scores: Dict[str, float]
    feedback: str
