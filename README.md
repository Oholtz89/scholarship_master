# Scholarship Master

Automated workflow for processing scholarship applications from Google Drive with intelligent document classification and AI-powered grading.

## Overview

This system automatically:
- ✅ Fetches scholarship applications from Google Drive
- ✅ Classifies documents into Essays, Transcripts, and Letters of Recommendation
- ✅ Extracts and analyzes document content
- ✅ Grades documents using AI with customizable scoring rubrics
- ✅ Stores all results in a searchable database

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Google Drive API credentials**
   - Download service account JSON from Google Cloud Console
   - Save as `service_account.json` in the project root

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Google Drive folder ID and OpenAI API key
   ```

4. **Run the workflow**
   ```bash
   python main.py
   ```

## Features

### Document Classification
Automatically categorizes documents using:
- File name and extension analysis
- MIME type detection
- Content analysis (AI-powered optional)

**Supported Categories:**
- Essays / Personal Statements
- Academic Transcripts
- Letters of Recommendation

### AI-Powered Grading
Uses OpenAI GPT-3.5 to evaluate documents based on:
- **Essays**: Clarity, Relevance, Depth, Grammar
- **Transcripts**: GPA, Course Rigor
- **Letters of Recommendation**: Strength, Specificity

### Database Management
SQLite database tracks:
- All submissions and applicants
- Document metadata and classifications
- Detailed scores and feedback

## Project Structure

```
scholarship_master/
├── src/
│   ├── config/          # Configuration & settings
│   ├── services/        # Core services (Drive, Classification, Grading)
│   ├── models/          # Data models & database schemas
│   ├── workflows/       # Workflow orchestration
│   ├── utils/           # Helper functions
│   └── agents/          # AI agents
├── main.py              # Entry point
├── requirements.txt     # Dependencies
└── SETUP.md            # Detailed setup guide
```

## Google Drive Structure

```
Your Submissions Folder/
├── John Doe - john@example.com/
│   ├── essay.pdf
│   ├── transcript.xlsx
│   └── recommendation.pdf
├── Jane Smith - jane@example.com/
│   ├── personal_statement.docx
│   └── transcript.pdf
└── ...
```

## Configuration

See [SETUP.md](SETUP.md) for detailed setup instructions and configuration options.

### Key Environment Variables
- `GOOGLE_DRIVE_FOLDER_ID`: Root submissions folder ID
- `OPENAI_API_KEY`: For AI-powered grading
- `GOOGLE_SERVICE_ACCOUNT_JSON`: Path to credentials

## Output Example

```
Applicant: John Doe (john@example.com)
Status: completed
Total Documents: 3
Overall Score: 245.0

Documents:
  - essay.pdf (Category: essay, Score: 87.5/100)
  - transcript.xlsx (Category: transcript, Score: 92/100)
  - recommendation_letter.pdf (Category: letter_of_recommendation, Score: 88/100)
```

## Architecture

### Services

- **GoogleDriveService**: API integration for fetching and downloading submissions
- **DocumentClassifier**: Intelligent document categorization
- **GradingAgent**: AI-powered document evaluation
- **DatabaseService**: Persistent storage and query management

### Workflow

The `SubmissionWorkflow` orchestrates the entire process:
1. List submissions from Google Drive
2. For each submission:
   - Fetch all documents
   - Classify each document
   - Extract and analyze content
   - Grade based on category
   - Store results in database

## Requirements

- Python 3.8+
- Google Drive API access
- OpenAI API key (optional but recommended)

## Dependencies

See [requirements.txt](requirements.txt) for full list:
- google-api-python-client
- openai
- SQLAlchemy
- pydantic
- python-dotenv

## Customization

### Custom Scoring Rubrics

Edit scoring criteria in `src/config/settings.py`:

```python
SCORING_RUBRIC = {
    "essay": {
        "max_score": 100,
        "criteria": {
            "clarity": {"weight": 0.25, "max": 25},
            # Customize as needed
        }
    }
}
```

### Document Categories

Modify classification rules in `src/config/settings.py`:

```python
DOCUMENT_CATEGORIES = {
    "custom_category": {
        "extensions": [".pdf", ".docx"],
        "keywords": ["keyword1", "keyword2"]
    }
}
```

## Troubleshooting

See the troubleshooting section in [SETUP.md](SETUP.md) for common issues and solutions.

## License

[Add your license here]

## Support

For detailed setup and troubleshooting, see [SETUP.md](SETUP.md)