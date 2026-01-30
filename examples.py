"""
Scholarship Master - Complete Workflow Configuration Example

This module shows how to use the scholarship submission workflow
with various configurations.
"""

from src.config import settings
from src.workflows import SubmissionWorkflow
from src.utils.report_generator import ReportGenerator, print_summary_report

# Example 1: Process submissions with default settings
def example_basic_workflow():
    """Process submissions using default Google Drive folder."""
    workflow = SubmissionWorkflow()
    submission_ids = workflow.process_submissions()
    
    for submission_id in submission_ids:
        summary = workflow.get_submission_summary(submission_id)
        print(f"Processed submission {submission_id}: {summary['applicant_name']}")


# Example 2: Process a specific folder
def example_process_specific_folder(folder_id: str):
    """Process a specific Google Drive folder."""
    workflow = SubmissionWorkflow()
    submission_ids = workflow.process_submissions(folder_id)
    print(f"Processed {len(submission_ids)} submissions from folder {folder_id}")


# Example 3: Generate reports
def example_generate_reports():
    """Generate and display reports."""
    print_summary_report()


# Example 4: Custom database queries
def example_database_queries():
    """Query database directly."""
    from src.services import DatabaseService
    
    db = DatabaseService()
    
    # Get all submissions
    submissions = db.list_submissions()
    print(f"Total submissions: {len(submissions)}")
    
    # Get submissions by status
    completed = db.list_submissions(status="completed")
    print(f"Completed submissions: {len(completed)}")
    
    # Get specific submission
    if submissions:
        submission = db.get_submission(submissions[0].id)
        print(f"Submission: {submission.applicant_name}")
        print(f"Documents: {len(submission.documents)}")


# Example 5: Customize scoring rubrics
def example_custom_rubrics():
    """Demonstrate custom rubric configuration."""
    
    # You can override rubrics in src/config/settings.py
    # Example custom rubric:
    custom_rubric = {
        "essay": {
            "max_score": 100,
            "criteria": {
                "originality": {"weight": 0.3, "max": 30},
                "writing_quality": {"weight": 0.3, "max": 30},
                "alignment_with_mission": {"weight": 0.4, "max": 40},
            }
        }
    }
    
    print("Custom rubric example:")
    print(custom_rubric)


# Example 6: Grade individual document
def example_grade_document():
    """Grade a single document."""
    from src.services import GradingAgent
    
    grading_agent = GradingAgent()
    
    sample_essay = """
    I believe leadership is about inspiring others to achieve their potential.
    Throughout my high school career, I have led the robotics team to regional
    championships and mentored younger students. This experience taught me that
    effective leaders listen, adapt, and empower their team members.
    """
    
    result = grading_agent.grade_document(
        "essay",
        sample_essay,
        "sample_essay.pdf"
    )
    
    print(f"Score: {result['total_score']}/{result['max_score']}")
    print(f"Feedback: {result['feedback']}")


# Example 7: Classify document
def example_classify_document():
    """Classify a document."""
    from src.services import DocumentClassifier
    
    classifier = DocumentClassifier()
    
    # Rule-based classification
    category = classifier.classify(
        "my_personal_essay.pdf",
        mime_type="application/pdf",
        content="This is my personal essay about..."
    )
    
    print(f"Classified as: {category}")
    
    # AI-based classification (requires OpenAI)
    result = classifier.classify_by_ai(
        "my_personal_essay.pdf",
        "This is my personal essay about my journey..."
    )
    
    print(f"AI classified as: {result['category']} (confidence: {result['confidence']})")


if __name__ == "__main__":
    print("Scholarship Master - Configuration Examples")
    print("=" * 60)
    print()
    
    print("Available examples:")
    print("1. example_basic_workflow() - Process submissions with defaults")
    print("2. example_process_specific_folder(folder_id) - Process specific folder")
    print("3. example_generate_reports() - Generate reports")
    print("4. example_database_queries() - Query database")
    print("5. example_custom_rubrics() - Show custom rubrics")
    print("6. example_grade_document() - Grade single document")
    print("7. example_classify_document() - Classify document")
    print()
    print("See source code comments for usage examples.")
