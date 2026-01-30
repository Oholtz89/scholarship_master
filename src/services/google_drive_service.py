"""Google Drive API service for accessing submissions."""
import io
import os
import logging
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from src.config import settings

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleDriveService:
    """Service for interacting with Google Drive API."""
    
    def __init__(self):
        """Initialize Google Drive service."""
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API using service account."""
        try:
            if os.path.exists(settings.GOOGLE_SERVICE_ACCOUNT_JSON):
                # Use service account
                credentials = Credentials.from_service_account_file(
                    settings.GOOGLE_SERVICE_ACCOUNT_JSON,
                    scopes=SCOPES
                )
            else:
                logger.warning("Service account JSON not found. Using OAuth flow.")
                credentials = self._oauth_authenticate()
            
            service = build("drive", "v3", credentials=credentials)
            logger.info("Successfully authenticated with Google Drive API")
            return service
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Drive: {e}")
            raise
    
    def _oauth_authenticate(self):
        """Authenticate using OAuth flow (for local development)."""
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )
        credentials = flow.run_local_server(port=0)
        return credentials
    
    def list_submissions(self, folder_id: Optional[str] = None) -> List[Dict]:
        """
        List all submission folders in the specified Google Drive folder.
        
        Args:
            folder_id: Google Drive folder ID. Uses GOOGLE_DRIVE_FOLDER_ID if not provided.
        
        Returns:
            List of folder metadata dictionaries.
        """
        folder_id = folder_id or settings.GOOGLE_DRIVE_FOLDER_ID
        
        try:
            query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces="drive",
                fields="files(id, name, createdTime, modifiedTime)",
                pageSize=1000
            ).execute()
            
            folders = results.get("files", [])
            logger.info(f"Found {len(folders)} submission folders")
            return folders
        except Exception as e:
            logger.error(f"Error listing submissions: {e}")
            raise
    
    def list_documents(self, folder_id: str) -> List[Dict]:
        """
        List all documents in a submission folder.
        
        Args:
            folder_id: Google Drive folder ID containing documents.
        
        Returns:
            List of file metadata dictionaries.
        """
        try:
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces="drive",
                fields="files(id, name, mimeType, size, createdTime)",
                pageSize=1000
            ).execute()
            
            files = results.get("files", [])
            logger.info(f"Found {len(files)} documents in folder {folder_id}")
            return files
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            raise
    
    def download_file(self, file_id: str, file_name: str, destination_path: str = "downloads") -> str:
        """
        Download a file from Google Drive.
        
        Args:
            file_id: Google Drive file ID.
            file_name: Name of the file.
            destination_path: Local path to save the file.
        
        Returns:
            Path to the downloaded file.
        """
        try:
            os.makedirs(destination_path, exist_ok=True)
            file_path = os.path.join(destination_path, file_name)
            
            request = self.service.files().get_media(fileId=file_id)
            file_handle = io.FileIO(file_path, "wb")
            downloader = MediaIoBaseDownload(file_handle, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            file_handle.close()
            logger.info(f"Downloaded {file_name} to {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error downloading file {file_id}: {e}")
            raise
    
    def get_file_content(self, file_id: str) -> bytes:
        """
        Get file content as bytes from Google Drive.
        
        Args:
            file_id: Google Drive file ID.
        
        Returns:
            File content as bytes.
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_handle = io.BytesIO()
            downloader = MediaIoBaseDownload(file_handle, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            return file_handle.getvalue()
        except Exception as e:
            logger.error(f"Error getting file content {file_id}: {e}")
            raise
