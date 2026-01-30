"""Database service for managing submissions and scores."""
import logging
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config import settings
from src.models.database import Base, SubmissionORM, DocumentORM, ScoreORM
from src.models.schemas import Submission, Document, Score

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations."""
    
    def __init__(self):
        """Initialize database service."""
        self.engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
        )
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self) -> Session:
        """Get a database session."""
        return self.SessionLocal()
    
    # Submission methods
    def create_submission(self, submission: Submission) -> int:
        """Create a new submission record."""
        db = self.get_session()
        try:
            db_submission = SubmissionORM(
                applicant_name=submission.applicant_name,
                applicant_email=submission.applicant_email,
                submission_folder_id=submission.submission_folder_id,
                status=submission.status,
            )
            db.add(db_submission)
            db.commit()
            db.refresh(db_submission)
            logger.info(f"Created submission {db_submission.id} for {submission.applicant_name}")
            return db_submission.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating submission: {e}")
            raise
        finally:
            db.close()
    
    def get_submission(self, submission_id: int) -> Optional[Submission]:
        """Get a submission by ID."""
        db = self.get_session()
        try:
            db_submission = db.query(SubmissionORM).filter(SubmissionORM.id == submission_id).first()
            if db_submission:
                return self._orm_to_schema(db_submission)
            return None
        finally:
            db.close()
    
    def get_submission_by_folder_id(self, folder_id: str) -> Optional[Submission]:
        """Get a submission by Google Drive folder ID."""
        db = self.get_session()
        try:
            db_submission = db.query(SubmissionORM).filter(
                SubmissionORM.submission_folder_id == folder_id
            ).first()
            if db_submission:
                return self._orm_to_schema(db_submission)
            return None
        finally:
            db.close()
    
    def list_submissions(self, status: Optional[str] = None) -> List[Submission]:
        """List all submissions, optionally filtered by status."""
        db = self.get_session()
        try:
            query = db.query(SubmissionORM)
            if status:
                query = query.filter(SubmissionORM.status == status)
            
            db_submissions = query.all()
            return [self._orm_to_schema(s) for s in db_submissions]
        finally:
            db.close()
    
    def update_submission_status(self, submission_id: int, status: str, error_message: Optional[str] = None) -> None:
        """Update submission status."""
        db = self.get_session()
        try:
            db_submission = db.query(SubmissionORM).filter(SubmissionORM.id == submission_id).first()
            if db_submission:
                db_submission.status = status
                if error_message:
                    db_submission.error_message = error_message
                db.commit()
                logger.info(f"Updated submission {submission_id} status to {status}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating submission: {e}")
            raise
        finally:
            db.close()
    
    # Document methods
    def create_document(self, submission_id: int, document: Document) -> int:
        """Create a new document record."""
        db = self.get_session()
        try:
            db_document = DocumentORM(
                submission_id=submission_id,
                name=document.name,
                google_drive_id=document.google_drive_id,
                mime_type=document.mime_type,
                category=document.category,
                file_size=document.file_size,
            )
            db.add(db_document)
            db.commit()
            db.refresh(db_document)
            logger.info(f"Created document {db_document.id} for submission {submission_id}")
            return db_document.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating document: {e}")
            raise
        finally:
            db.close()
    
    def get_document(self, document_id: int) -> Optional[Document]:
        """Get a document by ID."""
        db = self.get_session()
        try:
            db_document = db.query(DocumentORM).filter(DocumentORM.id == document_id).first()
            if db_document:
                return self._document_orm_to_schema(db_document)
            return None
        finally:
            db.close()
    
    def list_documents(self, submission_id: int) -> List[Document]:
        """List documents for a submission."""
        db = self.get_session()
        try:
            db_documents = db.query(DocumentORM).filter(DocumentORM.submission_id == submission_id).all()
            return [self._document_orm_to_schema(d) for d in db_documents]
        finally:
            db.close()
    
    def update_document(self, document_id: int, **kwargs) -> None:
        """Update document fields."""
        db = self.get_session()
        try:
            db_document = db.query(DocumentORM).filter(DocumentORM.id == document_id).first()
            if db_document:
                for key, value in kwargs.items():
                    if hasattr(db_document, key):
                        setattr(db_document, key, value)
                db.commit()
                logger.info(f"Updated document {document_id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating document: {e}")
            raise
        finally:
            db.close()
    
    # Score methods
    def create_score(self, submission_id: int, score: Score) -> int:
        """Create a new score record."""
        db = self.get_session()
        try:
            db_score = ScoreORM(
                submission_id=submission_id,
                document_id=score.document_id,
                category=score.category,
                total_score=score.total_score,
                max_score=score.max_score,
                criteria_scores=score.criteria_scores,
                feedback=score.feedback,
            )
            db.add(db_score)
            db.commit()
            db.refresh(db_score)
            logger.info(f"Created score {db_score.id} for document {score.document_id}")
            return db_score.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating score: {e}")
            raise
        finally:
            db.close()
    
    def get_scores(self, document_id: int) -> List[Score]:
        """Get scores for a document."""
        db = self.get_session()
        try:
            db_scores = db.query(ScoreORM).filter(ScoreORM.document_id == document_id).all()
            return [self._score_orm_to_schema(s) for s in db_scores]
        finally:
            db.close()
    
    def get_submission_scores(self, submission_id: int) -> List[Score]:
        """Get all scores for a submission."""
        db = self.get_session()
        try:
            db_scores = db.query(ScoreORM).filter(ScoreORM.submission_id == submission_id).all()
            return [self._score_orm_to_schema(s) for s in db_scores]
        finally:
            db.close()
    
    # Helper methods
    def _orm_to_schema(self, db_submission: SubmissionORM) -> Submission:
        """Convert ORM submission to schema."""
        return Submission(
            id=db_submission.id,
            applicant_name=db_submission.applicant_name,
            applicant_email=db_submission.applicant_email,
            submission_folder_id=db_submission.submission_folder_id,
            status=db_submission.status,
            created_at=db_submission.created_at,
            updated_at=db_submission.updated_at,
            error_message=db_submission.error_message,
            documents=[self._document_orm_to_schema(d) for d in db_submission.documents],
            scores=[self._score_orm_to_schema(s) for s in db_submission.scores],
        )
    
    def _document_orm_to_schema(self, db_document: DocumentORM) -> Document:
        """Convert ORM document to schema."""
        return Document(
            id=db_document.id,
            name=db_document.name,
            google_drive_id=db_document.google_drive_id,
            mime_type=db_document.mime_type,
            category=db_document.category,
            submission_id=db_document.submission_id,
            downloaded_path=db_document.downloaded_path,
            file_size=db_document.file_size,
            created_at=db_document.created_at,
            processed=db_document.processed,
            error_message=db_document.error_message,
        )
    
    def _score_orm_to_schema(self, db_score: ScoreORM) -> Score:
        """Convert ORM score to schema."""
        return Score(
            id=db_score.id,
            document_id=db_score.document_id,
            category=db_score.category,
            total_score=db_score.total_score,
            max_score=db_score.max_score,
            criteria_scores=db_score.criteria_scores or {},
            feedback=db_score.feedback,
            created_at=db_score.created_at,
        )
