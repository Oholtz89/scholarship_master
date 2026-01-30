# Scholarship Master - Quick Reference Guide

## Common Commands

### Setup & Installation
```bash
# Quick setup (Linux/Mac)
bash setup.sh

# Quick setup (Windows)
setup.bat

# Manual Python setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Running the Workflow
```bash
# Process all submissions
python main.py

# Process specific folder
python main.py YOUR_FOLDER_ID

# Run in background (Linux/Mac)
nohup python main.py > workflow.log 2>&1 &
```

### Generating Reports
```bash
# Summary report
python cli.py report summary

# Query all submissions
python cli.py query all

# Query completed submissions
python cli.py query completed

# Query pending submissions
python cli.py query pending

# Query submissions with errors
python cli.py query error
```

### Database Operations
```bash
# View SQLite database
sqlite3 scholarship_submissions.db

# View all submissions
SELECT * FROM submissions;

# View documents for a submission
SELECT * FROM documents WHERE submission_id = 1;

# View scores
SELECT * FROM scores WHERE submission_id = 1;

# Export to CSV
.mode csv
.output report.csv
SELECT * FROM submissions;
.output stdout
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_services.py

# Run with verbose output
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_services.py::TestDocumentClassifier::test_classify_essay
```

### Docker Commands
```bash
# Build image
docker build -t scholarship-master .

# Run with Docker Compose
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f scholarship-processor

# Stop containers
docker-compose down

# Clean up
docker-compose down -v
```

### Environment & Configuration
```bash
# Create .env from template
cp .env.example .env

# Test configuration
python -c "from src.config import settings; print(settings.GOOGLE_DRIVE_FOLDER_ID)"

# View all settings
python -c "from src.config import settings; import json; print(json.dumps(settings.__dict__, indent=2, default=str))"
```

### Development
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python main.py

# Run examples
python examples.py

# Check code quality
python -m pylint src/

# Format code
python -m black src/

# Check dependencies
pip list
pip check
```

---

## Configuration File Locations

| File | Purpose | Edit When |
|------|---------|-----------|
| `.env` | Environment variables | Changing API keys, folder IDs |
| `src/config/settings.py` | Application settings | Changing categories, rubrics, rules |
| `requirements.txt` | Python dependencies | Adding new packages |
| `Dockerfile` | Container configuration | Deploying with Docker |
| `docker-compose.yml` | Container orchestration | Custom Docker setup |

---

## API Usage Examples

### Use as a Library
```python
# Import and use services directly
from src.workflows import SubmissionWorkflow

workflow = SubmissionWorkflow()
submission_ids = workflow.process_submissions()

for sub_id in submission_ids:
    summary = workflow.get_submission_summary(sub_id)
    print(summary)
```

### Classify a Document
```python
from src.services import DocumentClassifier

classifier = DocumentClassifier()
category = classifier.classify("essay.pdf", "application/pdf", "Essay content...")
print(f"Category: {category}")
```

### Grade a Document
```python
from src.services import GradingAgent

grader = GradingAgent()
result = grader.grade_document("essay", "Essay content...", "essay.pdf")
print(f"Score: {result['total_score']}/{result['max_score']}")
```

### Query Database
```python
from src.services import DatabaseService

db = DatabaseService()
submissions = db.list_submissions(status="completed")
for sub in submissions:
    print(f"{sub.applicant_name}: {len(sub.documents)} documents")
```

---

## Useful File Paths

```
Project Root: /workspaces/scholarship_master/

Source Code:
  src/services/           - Core services
  src/models/             - Data models
  src/workflows/          - Orchestration
  src/config/settings.py  - Configuration

Data Files:
  scholarship_submissions.db - SQLite database
  downloads/                  - Downloaded documents
  service_account.json        - Google credentials

Documentation:
  README.md           - Main documentation
  SETUP.md            - Setup guide
  API_REFERENCE.md    - API docs
  ARCHITECTURE.md     - Architecture details
  GETTING_STARTED.md  - Step-by-step guide
```

---

## Logging Levels

```python
# In .env file:
LOG_LEVEL=DEBUG       # Show all messages (verbose)
LOG_LEVEL=INFO        # Show important messages (default)
LOG_LEVEL=WARNING     # Show warnings and errors only
LOG_LEVEL=ERROR       # Show errors only
LOG_LEVEL=CRITICAL    # Show critical errors only
```

---

## Environment Variables Reference

```bash
# Required
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
GOOGLE_SERVICE_ACCOUNT_JSON=./service_account.json

# Optional
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=sqlite:///./scholarship_submissions.db
LOG_LEVEL=INFO
MAX_RETRIES=3
```

---

## Performance Tips

```bash
# Increase performance
# 1. Use PostgreSQL instead of SQLite (update DATABASE_URL)
# 2. Run in background with nohup
# 3. Use Docker for isolation
# 4. Set LOG_LEVEL=WARNING for production
# 5. Batch process large folders
```

---

## Backup & Restore

```bash
# Backup database
cp scholarship_submissions.db scholarship_submissions.db.backup

# Backup .env and credentials
tar -czf config_backup.tar.gz .env service_account.json

# Restore database
rm scholarship_submissions.db
cp scholarship_submissions.db.backup scholarship_submissions.db

# Reset database
rm scholarship_submissions.db
python main.py  # Creates new database
```

---

## Monitoring

```bash
# Monitor process
ps aux | grep python

# Monitor system resources
top -p $(pgrep -f "python main.py")

# View recent logs
tail -f workflow.log

# Count submissions in database
sqlite3 scholarship_submissions.db "SELECT COUNT(*) FROM submissions;"
```

---

## Troubleshooting Commands

```bash
# Check Python version
python --version

# Check if packages installed
pip list | grep -E "google|openai|sqlalchemy"

# Test Google Drive connection
python -c "from src.services import GoogleDriveService; GoogleDriveService()"

# Test OpenAI connection
python -c "import openai; openai.api_key='test'; print('OK')"

# View error logs
grep ERROR workflow.log

# Debug specific error
python -c "from src.config import settings; print(settings.GOOGLE_DRIVE_FOLDER_ID)"
```

---

## File Size Limits

- **Maximum file download size**: Depends on disk space
- **Database size**: No limit (but consider backups)
- **Log file size**: Unlimited (consider rotation)
- **Text extraction limit**: 5000 characters per document

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Authentication error | Check service_account.json exists and is valid |
| Folder not found | Verify GOOGLE_DRIVE_FOLDER_ID and share with service account |
| Import errors | Run `pip install -r requirements.txt` |
| Database locked | Stop all running instances, delete *.db-journal files |
| Low scores | Check if OpenAI key is valid, adjust rubrics |
| No documents found | Verify folder structure matches expected format |
| Slow processing | Use PostgreSQL, increase LOG_LEVEL, reduce text extraction |

---

## Recommended Folder Structure for Organization

```
scholarship_master/
├── credentials/           # Store credentials here
│   └── service_account.json
├── data/
│   ├── submissions/       # Database files
│   └── backups/          # Database backups
├── downloads/            # Downloaded documents
├── logs/                 # Log files
│   ├── processing.log
│   └── errors.log
├── reports/              # Generated reports
└── config/              # Configuration files
    └── custom_rubrics.json
```

---

## Update & Maintenance

```bash
# Update dependencies
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# Check for outdated packages
pip list --outdated

# Clean up
pip cache purge
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} +

# Regular backups (Linux/Mac)
# Add to crontab: 0 2 * * * cp /path/to/scholarship_submissions.db /backups/db_$(date +%Y%m%d).db
```

---

## Useful Aliases (Linux/Mac)

Add to your `.bashrc` or `.zshrc`:

```bash
# Activate virtual environment
alias activate_scholarship='cd /path/to/scholarship_master && source venv/bin/activate'

# Run workflow
alias process_submissions='python main.py'

# Generate report
alias scholarship_report='python cli.py report summary'

# View logs
alias scholarship_logs='tail -f workflow.log'

# Database query
alias scholarship_db='sqlite3 scholarship_submissions.db'

# Quick test
alias test_scholarship='python -m pytest tests/'
```

---

## Support Resources

- **Documentation**: See README.md, SETUP.md, API_REFERENCE.md
- **Examples**: Check examples.py for usage patterns
- **Tests**: View tests/test_services.py for test examples
- **Issues**: Check SETUP.md troubleshooting section
- **Code**: All code is documented with docstrings

---

## Quick Stats

```bash
# Count total submissions
sqlite3 scholarship_submissions.db "SELECT COUNT(*) as submissions FROM submissions;"

# Count total documents
sqlite3 scholarship_submissions.db "SELECT COUNT(*) as documents FROM documents;"

# Average score
sqlite3 scholarship_submissions.db "SELECT AVG(total_score) as avg_score FROM scores;"

# Submissions by status
sqlite3 scholarship_submissions.db "SELECT status, COUNT(*) FROM submissions GROUP BY status;"

# Score distribution
sqlite3 scholarship_submissions.db "SELECT category, COUNT(*) as count, AVG(total_score) as avg FROM scores GROUP BY category;"
```

---

**Remember**: Always backup your database before making changes! 💾
