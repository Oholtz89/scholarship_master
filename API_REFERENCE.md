"""
API Reference and Developer Guide for Scholarship Master

This module documents the main classes and functions available
for extending and customizing the scholarship submission workflow.
"""

"""
================================================================================
CORE SERVICES
================================================================================

1. GoogleDriveService
   Location: src/services/google_drive_service.py
   
   Purpose: Interface with Google Drive API
   
   Key Methods:
   - list_submissions(folder_id) -> List[Dict]
     List all submission folders in a Google Drive folder
     
   - list_documents(folder_id) -> List[Dict]
     List all documents in a submission folder
     
   - download_file(file_id, file_name, destination_path) -> str
     Download a file from Google Drive to local disk
     
   - get_file_content(file_id) -> bytes
     Get raw file content as bytes
   
   Example:
   ```python
   from src.services import GoogleDriveService
   
   drive = GoogleDriveService()
   submissions = drive.list_submissions("your_folder_id")
   for submission in submissions:
       documents = drive.list_documents(submission["id"])
       print(f"Found {len(documents)} documents")
   ```

================================================================================

2. DocumentClassifier
   Location: src/services/document_classifier.py
   
   Purpose: Categorize documents into predefined types
   
   Key Methods:
   - classify(file_name, mime_type, content) -> str
     Rule-based document classification
     Returns: "essay", "transcript", "letter_of_recommendation", or "other"
     
   - classify_by_ai(file_name, content) -> Dict
     AI-powered classification using OpenAI
     Returns: {"category": str, "confidence": float}
   
   Example:
   ```python
   from src.services import DocumentClassifier
   
   classifier = DocumentClassifier()
   
   # Rule-based
   category = classifier.classify(
       "my_essay.pdf",
       "application/pdf",
       "This essay is about..."
   )
   
   # AI-powered
   result = classifier.classify_by_ai(
       "my_essay.pdf",
       "This essay is about..."
   )
   print(f"Category: {result['category']}, Confidence: {result['confidence']}")
   ```

================================================================================

3. GradingAgent
   Location: src/services/grading_agent.py
   
   Purpose: Grade documents using customizable rubrics
   
   Key Methods:
   - grade_document(category, content, file_name) -> Dict
     Grade a document based on its category
     
     Returns: {
       "category": str,
       "total_score": float,
       "max_score": float,
       "criteria_scores": Dict[str, float],
       "feedback": str
     }
   
   Example:
   ```python
   from src.services import GradingAgent
   
   grader = GradingAgent()
   
   result = grader.grade_document(
       "essay",
       "My essay content here...",
       "my_essay.pdf"
   )
   
   print(f"Score: {result['total_score']}/{result['max_score']}")
   print(f"Feedback: {result['feedback']}")
   ```

================================================================================

4. DatabaseService
   Location: src/services/database_service.py
   
   Purpose: Manage persistent storage of submissions and scores
   
   Key Methods:
   
   Submissions:
   - create_submission(submission: Submission) -> int
   - get_submission(submission_id: int) -> Optional[Submission]
   - get_submission_by_folder_id(folder_id: str) -> Optional[Submission]
   - list_submissions(status: Optional[str]) -> List[Submission]
   - update_submission_status(submission_id: int, status: str, error_message)
   
   Documents:
   - create_document(submission_id: int, document: Document) -> int
   - get_document(document_id: int) -> Optional[Document]
   - list_documents(submission_id: int) -> List[Document]
   - update_document(document_id: int, **kwargs)
   
   Scores:
   - create_score(submission_id: int, score: Score) -> int
   - get_scores(document_id: int) -> List[Score]
   - get_submission_scores(submission_id: int) -> List[Score]
   
   Example:
   ```python
   from src.services import DatabaseService
   from src.models.schemas import Submission, Document, Score
   
   db = DatabaseService()
   
   # Create submission
   submission = Submission(
       applicant_name="John Doe",
       applicant_email="john@example.com",
       submission_folder_id="folder_123"
   )
   submission_id = db.create_submission(submission)
   
   # Create document
   document = Document(
       name="essay.pdf",
       google_drive_id="file_123",
       mime_type="application/pdf",
       category="essay",
       submission_id=submission_id
   )
   document_id = db.create_document(submission_id, document)
   
   # Create score
   score = Score(
       document_id=document_id,
       category="essay",
       total_score=85.5,
       max_score=100,
       criteria_scores={"clarity": 22, "relevance": 20},
       feedback="Well-written essay with good structure"
   )
   db.create_score(submission_id, score)
   ```

================================================================================
WORKFLOW ORCHESTRATION
================================================================================

SubmissionWorkflow
   Location: src/workflows/submission_workflow.py
   
   Purpose: Orchestrate the complete submission processing pipeline
   
   Key Methods:
   - process_submissions(folder_id) -> List[int]
     Process all submissions in a Google Drive folder
     
   - get_submission_summary(submission_id) -> Dict
     Get complete summary of a submission with all documents and scores
   
   Workflow Steps:
   1. List submissions from Google Drive
   2. For each submission:
      - Fetch all documents
      - Classify each document
      - Extract text content
      - Grade based on category
      - Store in database
   
   Example:
   ```python
   from src.workflows import SubmissionWorkflow
   
   workflow = SubmissionWorkflow()
   
   # Process all submissions
   submission_ids = workflow.process_submissions()
   
   # Get summary of processed submissions
   for submission_id in submission_ids:
       summary = workflow.get_submission_summary(submission_id)
       print(summary)
   ```

================================================================================
DATA MODELS
================================================================================

Pydantic Schemas (for validation and serialization):
   Location: src/models/schemas.py
   
   - Submission
   - Document
   - Score
   - SubmissionBase, DocumentBase, ScoreBase (for creation)
   - GradingRequest, GradingResult

SQLAlchemy ORM Models (for database):
   Location: src/models/database.py
   
   - SubmissionORM
   - DocumentORM
   - ScoreORM

================================================================================
UTILITIES
================================================================================

1. TextExtractor
   Location: src/utils/text_extractor.py
   
   Purpose: Extract text from various document formats
   
   Supported Formats:
   - PDF (.pdf) - requires PyPDF2
   - Word (.docx) - requires python-docx
   - Text (.txt)
   - Excel (.xlsx, .xls) - requires openpyxl
   
   Example:
   ```python
   from src.utils import TextExtractor
   from src.services import GoogleDriveService
   
   extractor = TextExtractor()
   drive = GoogleDriveService()
   
   text = extractor.extract_text(
       "file_id_123",
       "document.pdf",
       drive
   )
   ```

2. ReportGenerator
   Location: src/utils/report_generator.py
   
   Purpose: Generate reports and analytics
   
   Methods:
   - generate_summary_report() -> Dict
   - generate_category_report() -> Dict[str, Dict]
   - get_top_applicants(limit: int) -> List[Dict]
   - print_summary_report() (prints to console)

================================================================================
CONFIGURATION
================================================================================

Settings Class
   Location: src/config/settings.py
   
   Key Configuration Variables:
   - GOOGLE_DRIVE_FOLDER_ID
   - GOOGLE_SERVICE_ACCOUNT_JSON
   - OPENAI_API_KEY
   - DATABASE_URL
   - LOG_LEVEL
   - MAX_RETRIES
   
   Customizable Configurations:
   - DOCUMENT_CATEGORIES: Modify document classification rules
   - SCORING_RUBRIC: Define custom scoring criteria
   
   Example - Custom Rubric:
   ```python
   from src.config import settings
   
   # Modify scoring rubric
   settings.SCORING_RUBRIC["essay"]["criteria"]["writing_quality"] = {
       "weight": 0.5,
       "max": 50
   }
   ```

================================================================================
EXTENDING THE SYSTEM
================================================================================

1. Add a New Document Category
   
   In src/config/settings.py:
   ```python
   DOCUMENT_CATEGORIES = {
       ...existing categories...,
       "portfolio": {
           "extensions": [".zip", ".pdf"],
           "keywords": ["portfolio", "project", "work sample"]
       }
   }
   
   SCORING_RUBRIC = {
       ...existing rubrics...,
       "portfolio": {
           "max_score": 100,
           "criteria": {
               "technical_quality": {"weight": 0.5, "max": 50},
               "creativity": {"weight": 0.5, "max": 50}
           }
       }
   }
   ```

2. Custom Grading Logic
   
   Create a new service extending GradingAgent:
   ```python
   from src.services import GradingAgent
   
   class CustomGradingAgent(GradingAgent):
       def grade_document(self, category, content, file_name):
           if category == "custom":
               return self._grade_custom(content)
           return super().grade_document(category, content, file_name)
       
       def _grade_custom(self, content):
           # Your custom grading logic here
           pass
   ```

3. Custom Classification Logic
   
   Extend DocumentClassifier:
   ```python
   from src.services import DocumentClassifier
   
   class CustomClassifier(DocumentClassifier):
       def classify(self, file_name, mime_type, content):
           # Your custom classification logic
           if some_condition:
               return "custom_category"
           return super().classify(file_name, mime_type, content)
   ```

4. Custom Database Queries
   
   Extend DatabaseService:
   ```python
   from src.services import DatabaseService
   
   class CustomDatabaseService(DatabaseService):
       def get_top_scorers(self, limit=10):
           db = self.get_session()
           try:
               # Your custom query logic
               pass
           finally:
               db.close()
   ```

================================================================================
ENVIRONMENT VARIABLES
================================================================================

Required:
- GOOGLE_DRIVE_FOLDER_ID: Google Drive folder ID containing submissions
- GOOGLE_SERVICE_ACCOUNT_JSON: Path to service account JSON file

Optional:
- OPENAI_API_KEY: For AI-powered classification and grading
- DATABASE_URL: Database connection string (default: SQLite)
- LOG_LEVEL: Logging level (INFO, DEBUG, WARNING, ERROR)
- MAX_RETRIES: Number of retries for failed operations

================================================================================
ERROR HANDLING
================================================================================

All services include error handling and logging:

- GoogleDriveService: Handles API authentication and network errors
- DocumentClassifier: Gracefully falls back to rule-based if AI unavailable
- GradingAgent: Returns partial results or fallback scores on error
- DatabaseService: Automatic rollback on transaction errors
- Workflow: Logs errors and continues processing other submissions

All errors are logged at the ERROR level with full context.

================================================================================
TESTING
================================================================================

Unit Tests
   Location: tests/test_services.py
   
   Run tests:
   ```bash
   python -m pytest tests/
   ```

Example Test:
```python
def test_classify_essay():
    classifier = DocumentClassifier()
    result = classifier.classify(
        "Personal_Essay.pdf",
        mime_type="application/pdf",
        content="This essay discusses..."
    )
    assert result == "essay"
```

================================================================================
"""
