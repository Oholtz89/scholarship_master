"""Main workflow for processing scholarship submissions."""
import logging
from typing import List, Optional

from src.services import GoogleDriveService, DocumentClassifier, GradingAgent, DatabaseService
from src.models.schemas import Submission, Document, Score
from src.utils.text_extractor import TextExtractor

logger = logging.getLogger(__name__)


class SubmissionWorkflow:
    """Orchestrates the entire submission processing workflow."""
    
    def __init__(self):
        """Initialize workflow with required services."""
        self.drive_service = GoogleDriveService()
        self.classifier = DocumentClassifier()
        self.grading_agent = GradingAgent()
        self.db_service = DatabaseService()
        self.text_extractor = TextExtractor()
    
    def process_submissions(self, folder_id: Optional[str] = None) -> List[int]:
        """
        Process all new submissions in a Google Drive folder.
        
        Args:
            folder_id: Google Drive folder ID. Uses default if not provided.
        
        Returns:
            List of processed submission IDs.
        """
        try:
            # Step 1: List all submission folders
            logger.info("Step 1: Fetching submissions from Google Drive...")
            submission_folders = self.drive_service.list_submissions(folder_id)
            
            processed_ids = []
            for folder in submission_folders:
                folder_id = folder["id"]
                folder_name = folder["name"]
                
                # Check if already processed
                existing = self.db_service.get_submission_by_folder_id(folder_id)
                if existing and existing.status in ["completed", "processing"]:
                    logger.info(f"Submission {folder_name} already processed")
                    continue
                
                # Process this submission
                try:
                    submission_id = self._process_single_submission(
                        folder_id,
                        folder_name,
                        existing
                    )
                    processed_ids.append(submission_id)
                except Exception as e:
                    logger.error(f"Error processing submission {folder_name}: {e}")
                    if existing:
                        self.db_service.update_submission_status(
                            existing.id,
                            "error",
                            str(e)
                        )
            
            logger.info(f"Processed {len(processed_ids)} submissions")
            return processed_ids
        
        except Exception as e:
            logger.error(f"Error in workflow: {e}")
            raise
    
    def _process_single_submission(self, folder_id: str, folder_name: str, existing: Optional[Submission]) -> int:
        """
        Process a single submission folder.
        
        Args:
            folder_id: Google Drive folder ID.
            folder_name: Name of the submission folder.
            existing: Existing submission record if any.
        
        Returns:
            Submission ID.
        """
        logger.info(f"Processing submission: {folder_name}")
        
        # Create or update submission record
        if existing:
            submission_id = existing.id
            self.db_service.update_submission_status(submission_id, "processing")
        else:
            # Extract applicant info from folder name (e.g., "John Doe - john@example.com")
            applicant_name = folder_name.split(" - ")[0] if " - " in folder_name else folder_name
            applicant_email = folder_name.split(" - ")[1] if " - " in folder_name else ""
            
            submission = Submission(
                applicant_name=applicant_name,
                applicant_email=applicant_email,
                submission_folder_id=folder_id,
                status="processing",
            )
            submission_id = self.db_service.create_submission(submission)
        
        # Step 2: List all documents in submission
        logger.info("Step 2: Fetching documents...")
        documents = self.drive_service.list_documents(folder_id)
        
        for doc in documents:
            self._process_document(submission_id, doc)
        
        # Mark submission as completed
        self.db_service.update_submission_status(submission_id, "completed")
        logger.info(f"Submission {submission_id} completed")
        
        return submission_id
    
    def _process_document(self, submission_id: int, doc_metadata: dict) -> None:
        """
        Process a single document: classify and grade it.
        
        Args:
            submission_id: ID of the parent submission.
            doc_metadata: File metadata from Google Drive.
        """
        doc_id = doc_metadata["id"]
        doc_name = doc_metadata["name"]
        mime_type = doc_metadata.get("mimeType", "")
        doc_size = doc_metadata.get("size", 0)
        
        logger.info(f"Processing document: {doc_name}")
        
        try:
            # Step 3: Classify document
            logger.info("Step 3: Classifying document...")
            
            # Download and extract text for better classification
            try:
                content = self.text_extractor.extract_text(doc_id, doc_name, self.drive_service)
            except Exception as e:
                logger.warning(f"Could not extract text from {doc_name}: {e}")
                content = ""
            
            category = self.classifier.classify(doc_name, mime_type, content)
            
            # Create document record
            document = Document(
                name=doc_name,
                google_drive_id=doc_id,
                mime_type=mime_type,
                category=category,
                submission_id=submission_id,
                file_size=doc_size,
            )
            document_id = self.db_service.create_document(submission_id, document)
            
            # Step 4: Grade document
            logger.info("Step 4: Grading document...")
            if category != "other" and content:
                grading_result = self.grading_agent.grade_document(
                    category,
                    content,
                    doc_name
                )
                
                # Save score
                score = Score(
                    document_id=document_id,
                    category=category,
                    total_score=grading_result["total_score"],
                    max_score=grading_result["max_score"],
                    criteria_scores=grading_result.get("criteria_scores", {}),
                    feedback=grading_result.get("feedback", ""),
                )
                self.db_service.create_score(submission_id, score)
                
                logger.info(f"Graded {doc_name}: {grading_result['total_score']}/{grading_result['max_score']}")
            
            # Mark document as processed
            self.db_service.update_document(document_id, processed=True)
        
        except Exception as e:
            logger.error(f"Error processing document {doc_name}: {e}")
            # Log the error but continue processing other documents
    
    def get_submission_summary(self, submission_id: int) -> dict:
        """
        Get a summary of a submission with all documents and scores.
        
        Args:
            submission_id: ID of the submission.
        
        Returns:
            Dictionary with submission summary.
        """
        submission = self.db_service.get_submission(submission_id)
        if not submission:
            return {}
        
        scores = self.db_service.get_submission_scores(submission_id)
        
        summary = {
            "submission_id": submission.id,
            "applicant_name": submission.applicant_name,
            "applicant_email": submission.applicant_email,
            "status": submission.status,
            "documents": [
                {
                    "id": doc.id,
                    "name": doc.name,
                    "category": doc.category,
                    "processed": doc.processed,
                    "scores": [s for s in scores if s.document_id == doc.id],
                }
                for doc in submission.documents
            ],
            "total_score": sum(s.total_score for s in scores),
            "document_count": len(submission.documents),
        }
        
        return summary
