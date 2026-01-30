"""Main entry point for the scholarship submission workflow."""
import logging
import sys
from typing import Optional

from src.workflows import SubmissionWorkflow
from src.config import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main(folder_id: Optional[str] = None):
    """
    Main workflow execution.
    
    Args:
        folder_id: Optional Google Drive folder ID. Uses default if not provided.
    """
    try:
        logger.info("Starting Scholarship Submission Workflow")
        logger.info(f"Database: {settings.DATABASE_URL}")
        
        # Initialize and run workflow
        workflow = SubmissionWorkflow()
        submission_ids = workflow.process_submissions(folder_id)
        
        # Print summaries
        logger.info("\n" + "=" * 80)
        logger.info("WORKFLOW SUMMARY")
        logger.info("=" * 80)
        
        for submission_id in submission_ids:
            summary = workflow.get_submission_summary(submission_id)
            print_submission_summary(summary)
        
        logger.info("=" * 80)
        logger.info(f"Processed {len(submission_ids)} submissions successfully")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        sys.exit(1)


def print_submission_summary(summary: dict):
    """Print a formatted submission summary."""
    if not summary:
        return
    
    print(f"\nApplicant: {summary['applicant_name']} ({summary['applicant_email']})")
    print(f"Status: {summary['status']}")
    print(f"Total Documents: {summary['document_count']}")
    print(f"Overall Score: {summary['total_score']:.1f}")
    print("\nDocuments:")
    
    for doc in summary['documents']:
        print(f"  - {doc['name']}")
        print(f"    Category: {doc['category']}")
        print(f"    Processed: {doc['processed']}")
        
        if doc['scores']:
            for score in doc['scores']:
                print(f"    Score: {score.total_score}/{score.max_score}")
                if score.feedback:
                    print(f"    Feedback: {score.feedback[:100]}...")


if __name__ == "__main__":
    folder_id = None
    if len(sys.argv) > 1:
        folder_id = sys.argv[1]
    
    main(folder_id)
