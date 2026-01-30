"""Application settings and configuration."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings from environment variables."""
    
    # Google Drive
    GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
    GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "service_account.json")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scholarship_submissions.db")
    
    # Application
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    # Document Categories
    DOCUMENT_CATEGORIES = {
        "essay": {"extensions": [".pdf", ".docx", ".txt"], "keywords": ["essay", "personal statement"]},
        "transcript": {"extensions": [".pdf", ".xlsx"], "keywords": ["transcript", "academic record", "gpa"]},
        "letter_of_recommendation": {"extensions": [".pdf", ".docx"], "keywords": ["letter", "recommendation", "reference"]},
        "other": {"extensions": [], "keywords": []},
    }
    
    # Scoring Configuration
    SCORING_RUBRIC = {
        "essay": {
            "max_score": 100,
            "criteria": {
                "clarity": {"weight": 0.25, "max": 25},
                "relevance": {"weight": 0.25, "max": 25},
                "depth": {"weight": 0.25, "max": 25},
                "grammar": {"weight": 0.25, "max": 25},
            }
        },
        "transcript": {
            "max_score": 100,
            "criteria": {
                "gpa": {"weight": 0.6, "max": 60},
                "course_rigor": {"weight": 0.4, "max": 40},
            }
        },
        "letter_of_recommendation": {
            "max_score": 100,
            "criteria": {
                "strength": {"weight": 0.5, "max": 50},
                "specificity": {"weight": 0.5, "max": 50},
            }
        },
    }


settings = Settings()
