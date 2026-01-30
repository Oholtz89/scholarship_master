# Scholarship Master - Getting Started Checklist

## ✅ Phase 1: Initial Setup (30 minutes)

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] Google account with admin access to Google Drive
- [ ] Text editor or IDE (VS Code recommended)
- [ ] Git installed (for version control)

### Step 1: Clone/Download Project
```bash
git clone <your-repo-url>
cd scholarship_master
```
- [ ] Project cloned successfully

### Step 2: Install Dependencies
```bash
# Option A: Using setup script (Recommended)
bash setup.sh                    # Linux/Mac
setup.bat                        # Windows

# Option B: Manual installation
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate.bat        # Windows
pip install -r requirements.txt
```
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] No installation errors

### Step 3: Verify Installation
```bash
python -c "import google.auth; import openai; import sqlalchemy; print('✓ All packages installed')"
```
- [ ] All packages verified

---

## 🔑 Phase 2: Google Drive Setup (45 minutes)

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. [ ] Created new project or selected existing project
3. [ ] Project name noted: `________________`

### Step 2: Enable Google Drive API
1. Navigate to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. [ ] Clicked "Enable"
4. [ ] API is now enabled

### Step 3: Create Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. [ ] Fill in service account details
   - Service account name: `________________`
   - Service account description: `________________`
4. [ ] Click "Create and Continue"
5. Grant basic editor role
6. [ ] Completed service account creation

### Step 4: Create and Download JSON Key
1. In service account details, go to "Keys" tab
2. Click "Add Key" → "Create new key" → "JSON"
3. [ ] JSON file downloaded
4. [ ] Saved as `service_account.json` in project root
5. [ ] File is in .gitignore (for security)

### Step 5: Share Google Drive Folder
1. Create a folder in Google Drive for submissions
2. [ ] Folder created: `________________`
3. [ ] Copy folder ID from URL: `________________`
4. Right-click folder → "Share"
5. Share with service account email (from JSON file):
   - [ ] Service account email: `________________`
6. Grant "Editor" access
7. [ ] Folder is shared with service account

---

## ⚙️ Phase 3: Configure Environment (15 minutes)

### Step 1: Create .env File
```bash
cp .env.example .env
```
- [ ] .env file created from template

### Step 2: Configure Required Variables
Edit `.env` and fill in:

```bash
# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=<paste_your_folder_id_here>
GOOGLE_SERVICE_ACCOUNT_JSON=./service_account.json

# OpenAI Configuration (Optional but Recommended)
OPENAI_API_KEY=sk-<your-api-key-here>

# Database Configuration
DATABASE_URL=sqlite:///./scholarship_submissions.db

# Application Configuration
LOG_LEVEL=INFO
```

- [ ] `GOOGLE_DRIVE_FOLDER_ID` filled in
- [ ] `GOOGLE_SERVICE_ACCOUNT_JSON` path correct
- [ ] `OPENAI_API_KEY` configured (or left blank for rule-based grading)
- [ ] Other settings reviewed

### Step 3: Verify Configuration
```bash
python -c "from src.config import settings; print(f'Drive ID: {settings.GOOGLE_DRIVE_FOLDER_ID}')"
```
- [ ] Configuration loads without errors

---

## 📁 Phase 4: Organize Google Drive (20 minutes)

### Expected Folder Structure
```
Your Submissions Folder/
├── John Doe - john@example.com/
│   ├── essay.pdf
│   ├── transcript.xlsx
│   └── recommendation_letter.pdf
├── Jane Smith - jane@example.com/
│   ├── personal_statement.docx
│   ├── transcript.pdf
│   └── letter_from_professor.pdf
└── Mike Johnson - mike@example.com/
    ├── application_essay.docx
    ├── transcript.xlsx
    └── two_recommendations.pdf
```

### Create Test Structure
1. [ ] Create at least 1 test applicant folder
   - [ ] Format: `FirstName LastName - email@example.com`
2. [ ] Add sample documents:
   - [ ] At least 1 essay/personal statement (PDF or DOCX)
   - [ ] At least 1 transcript (PDF or XLSX)
   - [ ] At least 1 letter of recommendation (PDF or DOCX)

### Verify Structure
- [ ] Folder names match expected format
- [ ] Documents have clear, descriptive names
- [ ] All files are readable by service account (shared folder)

---

## 🚀 Phase 5: Run First Workflow (15 minutes)

### Step 1: Activate Virtual Environment
```bash
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate.bat        # Windows
```
- [ ] Virtual environment activated (should see (venv) in prompt)

### Step 2: Run Workflow
```bash
python main.py
```
- [ ] Workflow started
- [ ] No authentication errors
- [ ] Documents being processed...
- [ ] [ ] Completion message displayed
- [ ] [ ] Submission summary shown

### What to Expect
You should see output like:
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

[... more documents ...]

================================================================================
WORKFLOW SUMMARY
================================================================================

Applicant: John Doe (john@example.com)
Status: completed
Total Documents: 3
Overall Score: 245.0

Documents:
  - essay.pdf (Category: essay, Score: 87.5/100)
  - transcript.xlsx (Category: transcript, Score: 92/100)
  - recommendation_letter.pdf (Category: letter_of_recommendation, Score: 88/100)
```

- [ ] Workflow completed successfully
- [ ] Documents classified correctly
- [ ] Scores calculated
- [ ] Database populated

---

## 📊 Phase 6: Generate Reports (10 minutes)

### View Database Results
```bash
python cli.py report summary
```
- [ ] Summary report displayed
- [ ] Statistics show correct submission count
- [ ] Scores are reasonable
- [ ] All categories represented

### Query Submissions
```bash
python cli.py query completed
```
- [ ] Query returned results
- [ ] Completed submissions listed

---

## 🔧 Phase 7: Customization (Optional - 30+ minutes)

### Customize Document Categories
Edit `src/config/settings.py`:
```python
DOCUMENT_CATEGORIES = {
    "essay": {"extensions": [".pdf", ".docx"], "keywords": [...]},
    # Add custom categories here
}
```
- [ ] Added/modified document categories as needed

### Customize Scoring Rubrics
Edit `src/config/settings.py`:
```python
SCORING_RUBRIC = {
    "essay": {
        "max_score": 100,
        "criteria": {...}
    }
    # Modify criteria and weights as needed
}
```
- [ ] Updated scoring rubrics to match your requirements

### Test Custom Configuration
```bash
python main.py
```
- [ ] Custom configuration working
- [ ] New categories recognized
- [ ] New scoring criteria applied

---

## 📚 Phase 8: Documentation Review (15 minutes)

Read key documentation:
- [ ] README.md - Project overview
- [ ] SETUP.md - Detailed setup guide
- [ ] API_REFERENCE.md - API documentation
- [ ] ARCHITECTURE.md - System architecture
- [ ] PROJECT_SUMMARY.md - Complete project summary

---

## 🐳 Phase 9: Docker Setup (Optional - 30 minutes)

If deploying with Docker:

### Build Image
```bash
docker build -t scholarship-master .
```
- [ ] Image built successfully

### Run with Docker Compose
```bash
docker-compose up
```
- [ ] Container started
- [ ] Workflow executed inside container
- [ ] Results visible

---

## ✨ Phase 10: Production Checklist (15 minutes)

Before going to production:

### Security
- [ ] `.env` file in `.gitignore`
- [ ] `service_account.json` in `.gitignore`
- [ ] No credentials in code
- [ ] API keys rotated regularly

### Performance
- [ ] LOG_LEVEL set appropriately
- [ ] Database backed up
- [ ] Error handling tested

### Monitoring
- [ ] Log files configured
- [ ] Error alerts set up
- [ ] Database size monitored

### Documentation
- [ ] System documented
- [ ] Runbooks created
- [ ] Emergency procedures documented

---

## 🎉 Completion

### Final Verification
- [ ] All phases completed
- [ ] First workflow successful
- [ ] Reports generated correctly
- [ ] Documentation reviewed
- [ ] System customized to your needs

### Next Actions
- [ ] Upload real scholarship applications
- [ ] Run workflow on production data
- [ ] Train team on system usage
- [ ] Set up automated scheduling (optional)
- [ ] Monitor system performance

---

## 📞 Troubleshooting Quick Links

If you encounter issues:

1. **Authentication Errors** → See SETUP.md "Troubleshooting" section
2. **Classification Issues** → See API_REFERENCE.md DocumentClassifier section
3. **Database Issues** → See SETUP.md Database Configuration section
4. **API Rate Limiting** → Check OpenAI account usage
5. **Text Extraction Failures** → See src/utils/text_extractor.py

---

## 🎓 Learning Resources

- Python: https://python.org/doc
- Google Drive API: https://developers.google.com/drive
- OpenAI API: https://openai.com/docs
- SQLAlchemy: https://sqlalchemy.org/
- FastAPI/Pydantic: https://pydantic-docs.helpmanual.io/

---

**Congratulations!** Your Scholarship Master system is now set up and ready to process scholarship applications! 🎊
