"""Services for business logic."""
from .google_drive_service import GoogleDriveService
from .document_classifier import DocumentClassifier
from .grading_agent import GradingAgent
# Use the lightweight JSON-backed DatabaseService for a simpler workflow
from .simple_database_service import DatabaseService

__all__ = [
    "GoogleDriveService",
    "DocumentClassifier",
    "GradingAgent",
    "DatabaseService",
]
