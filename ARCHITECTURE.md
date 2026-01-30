"""
Scholarship Master - Complete Project Structure and File Guide

This file documents the complete structure of the scholarship submission
processing system and explains the purpose of each component.
"""

PROJECT_STRUCTURE = """
scholarship_master/
│
├── src/                           # Main application code
│   ├── __init__.py
│   │
│   ├── config/                    # Configuration module
│   │   ├── __init__.py
│   │   └── settings.py            # Environment variables and settings
│   │
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   ├── schemas.py             # Pydantic validation schemas
│   │   └── database.py            # SQLAlchemy ORM models
│   │
│   ├── services/                  # Core business logic services
│   │   ├── __init__.py
│   │   ├── google_drive_service.py    # Google Drive API integration
│   │   ├── document_classifier.py     # Document categorization
│   │   ├── grading_agent.py           # AI-powered document grading
│   │   └── database_service.py        # Database operations
│   │
│   ├── workflows/                 # Workflow orchestration
│   │   ├── __init__.py
│   │   └── submission_workflow.py    # Main workflow coordinator
│   │
│   ├── agents/                    # AI agents (extensible)
│   │   └── __init__.py
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── text_extractor.py      # Extract text from documents
│       └── report_generator.py    # Generate reports and analytics
│
├── tests/                         # Unit tests
│   └── test_services.py           # Service tests
│
├── data/                          # Data directory
│   └── (database files stored here)
│
├── main.py                        # Application entry point
├── cli.py                         # Command-line interface
├── examples.py                    # Usage examples
│
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── Dockerfile                     # Docker containerization
├── docker-compose.yml             # Docker Compose configuration
│
├── setup.sh                       # Linux/Mac setup script
├── setup.bat                      # Windows setup script
│
├── README.md                      # Main project documentation
├── SETUP.md                       # Detailed setup guide
└── API_REFERENCE.md              # API documentation

"""

FILE_PURPOSES = {
    "src/config/settings.py": """
    Contains all configuration variables loaded from environment.
    
    Key Variables:
    - Google Drive configuration (folder ID, credentials)
    - OpenAI API key
    - Database connection URL
    - Document categories and keywords
    - Scoring rubrics for each document type
    - Log level and retry settings
    
    This is the main place to customize the system's behavior.
    """,
    
    "src/models/schemas.py": """
    Pydantic models for data validation and serialization.
    
    Models:
    - Submission: Applicant submission
    - Document: Individual document in submission
    - Score: Document grading result
    - GradingRequest/Result: API contracts
    
    Used for validation and type safety throughout the application.
    """,
    
    "src/models/database.py": """
    SQLAlchemy ORM models for database persistence.
    
    Tables:
    - SubmissionORM: Stores applicant submissions
    - DocumentORM: Stores individual documents
    - ScoreORM: Stores document scores and feedback
    
    Handles database schema and relationships.
    """,
    
    "src/services/google_drive_service.py": """
    Interface with Google Drive API.
    
    Responsibilities:
    - Authenticate with Google Drive
    - List submission folders
    - List documents in folders
    - Download files from Drive
    - Extract file content
    
    Main entry point for interacting with user's Google Drive.
    """,
    
    "src/services/document_classifier.py": """
    Classify documents into predefined categories.
    
    Responsibilities:
    - Rule-based classification (keywords, extensions)
    - AI-based classification (OpenAI GPT-3.5)
    - Determine document category (essay, transcript, etc.)
    
    Key categories: essay, transcript, letter_of_recommendation, other
    """,
    
    "src/services/grading_agent.py": """
    Grade documents using customizable rubrics.
    
    Responsibilities:
    - Grade documents based on category
    - Use AI for detailed analysis and feedback
    - Fall back to rule-based grading if AI unavailable
    - Return scores and detailed feedback
    
    Uses customizable scoring rubrics from settings.
    """,
    
    "src/services/database_service.py": """
    Manage all database operations.
    
    Responsibilities:
    - CRUD operations for submissions, documents, scores
    - Query and filtering
    - Database session management
    - ORM to schema conversion
    
    Single interface for all database interactions.
    """,
    
    "src/workflows/submission_workflow.py": """
    Orchestrate the complete submission processing pipeline.
    
    Workflow Steps:
    1. List submissions from Google Drive
    2. For each submission:
       - Fetch documents
       - Classify documents
       - Extract text content
       - Grade documents
       - Store results in database
    3. Generate summary reports
    
    Coordinates all services to process submissions end-to-end.
    """,
    
    "src/utils/text_extractor.py": """
    Extract text from various document formats.
    
    Supported Formats:
    - PDF (.pdf) - uses PyPDF2
    - Word (.docx) - uses python-docx
    - Text (.txt) - plain text
    - Excel (.xlsx, .xls) - uses openpyxl
    
    Provides text for classification and grading.
    """,
    
    "src/utils/report_generator.py": """
    Generate reports and analytics from submission data.
    
    Reports:
    - Summary report (overall statistics)
    - Category report (scores by document type)
    - Top applicants ranking
    - Custom queries
    
    Used for analysis and decision-making.
    """,
    
    "main.py": """
    Main application entry point.
    
    Responsibilities:
    - Initialize workflow
    - Process submissions
    - Display results
    - Handle command-line arguments
    
    Usage: python main.py [optional_folder_id]
    """,
    
    "cli.py": """
    Command-line interface for reports and queries.
    
    Commands:
    - report summary: Overall statistics
    - report category: Scores by category
    - report applicants: Top applicants
    - query [status]: Filter submissions
    
    Usage: python cli.py report summary
    """,
    
    "requirements.txt": """
    Python package dependencies.
    
    Core:
    - google-api-python-client: Google Drive API
    - openai: OpenAI API for grading
    - SQLAlchemy: Database ORM
    - pydantic: Data validation
    
    Document Processing:
    - PyPDF2: PDF text extraction
    - python-docx: Word document handling
    - openpyxl: Excel file handling
    
    Other:
    - python-dotenv: Environment variable management
    """,
    
    ".env.example": """
    Template for environment variables.
    
    Variables:
    - GOOGLE_DRIVE_FOLDER_ID: Root submissions folder
    - GOOGLE_SERVICE_ACCOUNT_JSON: Path to credentials
    - OPENAI_API_KEY: API key for AI grading
    - DATABASE_URL: Database connection string
    - LOG_LEVEL: Logging level
    
    Copy to .env and customize for your setup.
    """,
    
    "Dockerfile": """
    Docker container definition.
    
    Image: python:3.11-slim
    
    Includes:
    - Python 3.11
    - All dependencies from requirements.txt
    - Application code
    - Environment configuration
    
    Usage: docker build -t scholarship-master .
    """,
    
    "docker-compose.yml": """
    Docker Compose orchestration.
    
    Services:
    - scholarship-processor: Main application container
    
    Volumes:
    - service_account.json (read-only)
    - data/: Database storage
    - downloads/: Downloaded documents
    
    Usage: docker-compose up
    """,
    
    "setup.sh": """
    Linux/Mac quick setup script.
    
    Steps:
    1. Check Python installation
    2. Create virtual environment
    3. Install dependencies
    4. Create .env file
    5. Display next steps
    
    Usage: bash setup.sh
    """,
    
    "setup.bat": """
    Windows quick setup script.
    
    Same as setup.sh but for Windows CMD.
    
    Usage: setup.bat
    """,
    
    "README.md": """
    Main project documentation.
    
    Includes:
    - Project overview
    - Quick start guide
    - Feature list
    - Project structure
    - Configuration info
    - Customization guide
    - Troubleshooting
    
    Starting point for new users.
    """,
    
    "SETUP.md": """
    Detailed setup and configuration guide.
    
    Includes:
    - Installation steps
    - Google Drive API setup
    - Configuration details
    - Expected folder structure
    - Usage examples
    - Troubleshooting
    - Advanced features
    
    Reference for detailed setup.
    """,
    
    "API_REFERENCE.md": """
    Complete API documentation.
    
    Includes:
    - Service class documentation
    - Method signatures
    - Usage examples
    - Data models
    - Configuration options
    - Extension guide
    - Error handling
    - Testing
    
    Reference for developers extending the system.
    """,
}

DATA_FLOW = """
Data Flow Through the System:

1. INITIATION
   User runs: python main.py
   
2. GOOGLE DRIVE FETCH
   GoogleDriveService.list_submissions()
   -> Gets all submission folders from configured Drive folder
   -> For each folder: GoogleDriveService.list_documents()
   
3. DOCUMENT PROCESSING (per document)
   a) CLASSIFICATION
      DocumentClassifier.classify(file_name, mime_type, content)
      -> Returns: essay | transcript | letter_of_recommendation | other
   
   b) TEXT EXTRACTION
      TextExtractor.extract_text(file_id, file_name, drive_service)
      -> Returns: Plain text content for analysis
   
   c) GRADING
      GradingAgent.grade_document(category, content, file_name)
      -> Returns: {total_score, criteria_scores, feedback}
   
4. DATABASE STORAGE
   DatabaseService.create_submission()
   DatabaseService.create_document()
   DatabaseService.create_score()
   -> Stores all data in SQLite database
   
5. REPORTING
   ReportGenerator.generate_summary_report()
   -> Aggregates and presents results
   
6. OUTPUT
   Display summaries and statistics to user

"""

DATABASE_SCHEMA = """
Database Schema:

submissions (Submission Records)
├── id (PRIMARY KEY)
├── applicant_name
├── applicant_email
├── submission_folder_id (UNIQUE)
├── status (pending | processing | completed | error)
├── error_message
├── created_at
└── updated_at

documents (Document Files)
├── id (PRIMARY KEY)
├── submission_id (FOREIGN KEY)
├── name
├── google_drive_id (UNIQUE)
├── mime_type
├── category (essay | transcript | letter_of_recommendation | other)
├── downloaded_path
├── file_size
├── processed (boolean)
├── error_message
└── created_at

scores (Grading Results)
├── id (PRIMARY KEY)
├── document_id (FOREIGN KEY)
├── submission_id (FOREIGN KEY)
├── category
├── total_score
├── max_score
├── criteria_scores (JSON)
├── feedback
└── created_at

Relationships:
- submission has many documents
- submission has many scores
- document has many scores
"""

WORKFLOW_SEQUENCE = """
Complete Workflow Sequence:

START
  │
  ├─→ Initialize Services
  │    ├─ GoogleDriveService()
  │    ├─ DocumentClassifier()
  │    ├─ GradingAgent()
  │    └─ DatabaseService()
  │
  ├─→ Fetch Submissions from Google Drive
  │    └─ list_submissions(folder_id)
  │
  ├─→ For Each Submission:
  │    │
  │    ├─→ Create/Update Submission Record
  │    │
  │    ├─→ Fetch Documents from Folder
  │    │
  │    ├─→ For Each Document:
  │    │    │
  │    │    ├─→ Download File (if needed)
  │    │    │
  │    │    ├─→ Extract Text Content
  │    │    │
  │    │    ├─→ Classify Document
  │    │    │    └─ Returns: category
  │    │    │
  │    │    ├─→ Create Document Record in DB
  │    │    │
  │    │    ├─→ Grade Document
  │    │    │    └─ Returns: scores & feedback
  │    │    │
  │    │    ├─→ Create Score Record in DB
  │    │    │
  │    │    └─→ Mark Document as Processed
  │    │
  │    └─→ Mark Submission as Completed
  │
  ├─→ Generate Summary Report
  │    ├─ Overall statistics
  │    ├─ Category breakdown
  │    └─ Top applicants
  │
  └─→ END

"""

if __name__ == "__main__":
    print(PROJECT_STRUCTURE)
    print("\n" + "=" * 80 + "\n")
    print("FILE PURPOSES:\n")
    for file, purpose in FILE_PURPOSES.items():
        print(f"\n{file}")
        print("-" * len(file))
        print(purpose)
    print("\n" + "=" * 80 + "\n")
    print(DATA_FLOW)
    print("\n" + "=" * 80 + "\n")
    print(DATABASE_SCHEMA)
    print("\n" + "=" * 80 + "\n")
    print(WORKFLOW_SEQUENCE)
