# Scholarship Master Setup Guide

This is a complete workflow system for processing scholarship applications from Google Drive and automatically classifying and grading submitted documents.

## Features

- **Google Drive Integration**: Automatically fetches submission folders and documents
- **Document Classification**: Categorizes documents into Essays, Transcripts, and Letters of Recommendation
- **AI-Powered Grading**: Uses OpenAI to grade documents based on customizable rubrics
- **Database Management**: Stores all submissions, documents, and scores for tracking
- **Workflow Orchestration**: Manages the entire processing pipeline

## Prerequisites

- Python 3.8+
- Google Drive API access
- OpenAI API key (optional, but recommended for AI grading)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd scholarship_master
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Drive API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Drive API
   - Create a Service Account and download the JSON credentials
   - Save the JSON file as `service_account.json` in the project root

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your settings:
   - `GOOGLE_DRIVE_FOLDER_ID`: The ID of your root submissions folder
   - `OPENAI_API_KEY`: Your OpenAI API key (for AI grading)
   - `GOOGLE_SERVICE_ACCOUNT_JSON`: Path to your service account JSON

## Google Drive Structure

The expected folder structure in Google Drive:

```
Submissions Folder (GOOGLE_DRIVE_FOLDER_ID)
├── John Doe - john@example.com/
│   ├── essay.pdf
│   ├── transcript.xlsx
│   └── recommendation_letter.pdf
├── Jane Smith - jane@example.com/
│   ├── personal_statement.docx
│   └── transcript.pdf
└── ...
```

**Folder naming format**: `Applicant Name - applicant@email.com`

## Usage

### Basic Usage

Run the workflow to process all submissions:

```bash
python main.py
```

### Process Specific Folder

Process a specific submission folder:

```bash
python main.py GOOGLE_DRIVE_FOLDER_ID
```

### Workflow Steps

The workflow automatically:

1. **Fetches submissions** from Google Drive
2. **Classifies documents** into categories (Essay, Transcript, Letter of Recommendation)
3. **Extracts text** from documents for analysis
4. **Grades documents** using AI or rule-based scoring
5. **Stores results** in the local database
6. **Generates summaries** of submissions

## Document Classification

Documents are automatically classified based on:

- **File name patterns** (contains keywords like "essay", "transcript", "letter")
- **MIME type** (PDF, DOCX, XLSX)
- **Content analysis** (AI-powered if OpenAI is configured)

### Supported Document Types

- **Essay**: Personal statements, essays (PDF, DOCX, TXT)
- **Transcript**: Academic transcripts, records (PDF, XLSX)
- **Letter of Recommendation**: Reference letters (PDF, DOCX)

## Scoring System

Each document category has its own scoring rubric:

### Essay (0-100)
- Clarity (25%)
- Relevance (25%)
- Depth (25%)
- Grammar (25%)

### Transcript (0-100)
- GPA (60%)
- Course Rigor (40%)

### Letter of Recommendation (0-100)
- Strength (50%)
- Specificity (50%)

Rubrics are defined in `src/config/settings.py` and can be customized.

## Database

The system uses SQLite by default (configurable via `DATABASE_URL`).

### Tables

- **submissions**: Applicant submissions
- **documents**: Individual documents
- **scores**: Document scores and feedback

View the database schema in `src/models/database.py`.

## API Services

### GoogleDriveService
- Lists submissions and documents
- Downloads files from Google Drive
- Extracts file content

### DocumentClassifier
- Rule-based classification
- AI-powered classification (with OpenAI)

### GradingAgent
- AI-powered grading with detailed feedback
- Rule-based fallback grading
- Customizable scoring rubrics

### DatabaseService
- CRUD operations for submissions, documents, and scores
- Query and filtering capabilities

## Configuration

### Document Categories

Edit `src/config/settings.py` to customize document categories:

```python
DOCUMENT_CATEGORIES = {
    "essay": {"extensions": [".pdf", ".docx"], "keywords": ["essay", "personal"]},
    # Add more categories...
}
```

### Scoring Rubrics

Customize scoring rubrics in `src/config/settings.py`:

```python
SCORING_RUBRIC = {
    "essay": {
        "max_score": 100,
        "criteria": {
            "clarity": {"weight": 0.25, "max": 25},
            # Add more criteria...
        }
    }
}
```

## Troubleshooting

### Google Drive Authentication Issues
- Verify `service_account.json` exists and has correct permissions
- Check that the service account has access to the Google Drive folder
- Ensure `GOOGLE_DRIVE_FOLDER_ID` is correct

### OpenAI Grading Issues
- Verify `OPENAI_API_KEY` is set correctly
- Check your OpenAI account has available credits
- System will fall back to rule-based grading if API is unavailable

### Text Extraction Issues
- Install additional dependencies if needed:
  ```bash
  pip install PyPDF2 python-docx openpyxl
  ```pt

### Database Issues
- Delete `scholarship_submissions.db` to reset the database
- Check file permissions for the data directory

## Logging

Logs are printed to the console. Adjust logging level in `.env`:

```
LOG_LEVEL=DEBUG  # or INFO, WARNING, ERROR
```

## Example Output

```
2024-01-30 10:15:00 - root - INFO - Starting Scholarship Submission Workflow
2024-01-30 10:15:01 - root - INFO - Step 1: Fetching submissions from Google Drive...
2024-01-30 10:15:03 - root - INFO - Processing submission: John Doe - john@example.com
2024-01-30 10:15:04 - root - INFO - Step 2: Fetching documents...
2024-01-30 10:15:05 - root - INFO - Processing document: essay.pdf
2024-01-30 10:15:06 - root - INFO - Step 3: Classifying document...
2024-01-30 10:15:07 - root - INFO - Classified 'essay.pdf' as essay
2024-01-30 10:15:08 - root - INFO - Step 4: Grading document...
2024-01-30 10:15:12 - root - INFO - Graded essay.pdf: 87.5/100

================================================================================
WORKFLOW SUMMARY
================================================================================

Applicant: John Doe (john@example.com)
Status: completed
Total Documents: 3
Overall Score: 245.0

Documents:
  - essay.pdf
    Category: essay
    Processed: True
    Score: 87.5/100
  - transcript.xlsx
    Category: transcript
    Processed: True
    Score: 92/100
  - recommendation_letter.pdf
    Category: letter_of_recommendation
    Processed: True
    Score: 88/100

================================================================================
Processed 1 submissions successfully
================================================================================
```

## Next Steps

1. Set up your Google Drive folder structure
2. Configure your API keys in `.env`
3. Run `python main.py` to process submissions
4. Review results in the database

## Support

For issues or questions, check the logs or review the code documentation in each module.
