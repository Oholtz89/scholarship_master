"""A lightweight in-memory DatabaseService replacement.

Stores submissions, documents, and scores in-memory and persists to
`data/store.json` for simple long-running runs without SQL.
"""
import json
import os
from typing import List, Optional
from datetime import datetime

from src.models.schemas import Submission, Document, Score


class DatabaseService:
    """Simple DatabaseService that mimics the original interface.

    Data is persisted to `data/store.json` so results survive process restarts.
    """

    FILE_PATH = os.path.join(os.getcwd(), "data", "store.json")

    def __init__(self):
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.FILE_PATH):
            try:
                with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        else:
            data = {}

        self.submissions = data.get("submissions", [])
        self.documents = data.get("documents", [])
        self.scores = data.get("scores", [])
        self.next_submission_id = data.get("next_submission_id", 1)
        self.next_document_id = data.get("next_document_id", 1)
        self.next_score_id = data.get("next_score_id", 1)

    def _save(self):
        data = {
            "submissions": self.submissions,
            "documents": self.documents,
            "scores": self.scores,
            "next_submission_id": self.next_submission_id,
            "next_document_id": self.next_document_id,
            "next_score_id": self.next_score_id,
        }
        tmp = self.FILE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, default=str, indent=2)
        os.replace(tmp, self.FILE_PATH)

    # Submission methods
    def create_submission(self, submission: Submission) -> int:
        sid = self.next_submission_id
        self.next_submission_id += 1

        item = {
            "id": sid,
            "applicant_name": submission.applicant_name,
            "applicant_email": submission.applicant_email,
            "submission_folder_id": submission.submission_folder_id,
            "status": submission.status,
            "created_at": submission.created_at.isoformat() if submission.created_at else datetime.utcnow().isoformat(),
            "updated_at": submission.updated_at.isoformat() if submission.updated_at else datetime.utcnow().isoformat(),
            "error_message": submission.error_message,
        }
        self.submissions.append(item)
        self._save()
        return sid

    def get_submission(self, submission_id: int) -> Optional[Submission]:
        s = next((x for x in self.submissions if x["id"] == submission_id), None)
        if not s:
            return None

        docs = [self._document_dict_to_schema(d) for d in self.documents if d["submission_id"] == submission_id]
        scores = [self._score_dict_to_schema(sc) for sc in self.scores if sc["submission_id"] == submission_id]

        return Submission(
            id=s["id"],
            applicant_name=s.get("applicant_name", ""),
            applicant_email=s.get("applicant_email", ""),
            submission_folder_id=s.get("submission_folder_id", ""),
            documents=docs,
            scores=scores,
            status=s.get("status", "pending"),
            created_at=datetime.fromisoformat(s.get("created_at")) if s.get("created_at") else datetime.utcnow(),
            updated_at=datetime.fromisoformat(s.get("updated_at")) if s.get("updated_at") else datetime.utcnow(),
            error_message=s.get("error_message"),
        )

    def get_submission_by_folder_id(self, folder_id: str) -> Optional[Submission]:
        s = next((x for x in self.submissions if x.get("submission_folder_id") == folder_id), None)
        if not s:
            return None
        return self.get_submission(s["id"])

    def list_submissions(self, status: Optional[str] = None) -> List[Submission]:
        items = self.submissions if status is None else [x for x in self.submissions if x.get("status") == status]
        return [self.get_submission(x["id"]) for x in items]

    def update_submission_status(self, submission_id: int, status: str, error_message: Optional[str] = None) -> None:
        s = next((x for x in self.submissions if x["id"] == submission_id), None)
        if s:
            s["status"] = status
            if error_message:
                s["error_message"] = error_message
            s["updated_at"] = datetime.utcnow().isoformat()
            self._save()

    # Document methods
    def create_document(self, submission_id: int, document: Document) -> int:
        did = self.next_document_id
        self.next_document_id += 1

        item = {
            "id": did,
            "submission_id": submission_id,
            "name": document.name,
            "google_drive_id": document.google_drive_id,
            "mime_type": document.mime_type,
            "category": document.category,
            "downloaded_path": document.downloaded_path,
            "file_size": document.file_size,
            "created_at": document.created_at.isoformat() if document.created_at else datetime.utcnow().isoformat(),
            "processed": bool(document.processed),
            "error_message": document.error_message,
        }
        self.documents.append(item)
        self._save()
        return did

    def get_document(self, document_id: int) -> Optional[Document]:
        d = next((x for x in self.documents if x["id"] == document_id), None)
        if not d:
            return None
        return self._document_dict_to_schema(d)

    def list_documents(self, submission_id: int) -> List[Document]:
        return [self._document_dict_to_schema(d) for d in self.documents if d["submission_id"] == submission_id]

    def update_document(self, document_id: int, **kwargs) -> None:
        d = next((x for x in self.documents if x["id"] == document_id), None)
        if d:
            for k, v in kwargs.items():
                if k in d:
                    d[k] = v
            self._save()

    # Score methods
    def create_score(self, submission_id: int, score: Score) -> int:
        sid = self.next_score_id
        self.next_score_id += 1

        item = {
            "id": sid,
            "document_id": score.document_id,
            "submission_id": submission_id,
            "category": score.category,
            "total_score": score.total_score,
            "max_score": score.max_score,
            "criteria_scores": score.criteria_scores,
            "feedback": score.feedback,
            "created_at": score.created_at.isoformat() if score.created_at else datetime.utcnow().isoformat(),
        }
        self.scores.append(item)
        self._save()
        return sid

    def get_scores(self, document_id: int) -> List[Score]:
        return [self._score_dict_to_schema(s) for s in self.scores if s["document_id"] == document_id]

    def get_submission_scores(self, submission_id: int) -> List[Score]:
        return [self._score_dict_to_schema(s) for s in self.scores if s["submission_id"] == submission_id]

    # Helpers to convert dicts to Pydantic schemas
    def _document_dict_to_schema(self, d: dict) -> Document:
        return Document(
            id=d.get("id"),
            name=d.get("name"),
            google_drive_id=d.get("google_drive_id"),
            mime_type=d.get("mime_type"),
            category=d.get("category"),
            submission_id=d.get("submission_id"),
            downloaded_path=d.get("downloaded_path"),
            file_size=d.get("file_size", 0),
            created_at=datetime.fromisoformat(d.get("created_at")) if d.get("created_at") else datetime.utcnow(),
            processed=d.get("processed", False),
            error_message=d.get("error_message"),
        )

    def _score_dict_to_schema(self, s: dict) -> Score:
        return Score(
            id=s.get("id"),
            document_id=s.get("document_id"),
            category=s.get("category"),
            total_score=s.get("total_score", 0.0),
            max_score=s.get("max_score", 100.0),
            criteria_scores=s.get("criteria_scores", {}),
            feedback=s.get("feedback"),
            created_at=datetime.fromisoformat(s.get("created_at")) if s.get("created_at") else datetime.utcnow(),
        )
