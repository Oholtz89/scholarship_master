"""Service for classifying documents into categories."""
import logging
import os
from typing import Dict, Optional

from src.config import settings

logger = logging.getLogger(__name__)


class DocumentClassifier:
    """Classify documents into predefined categories."""
    
    def __init__(self):
        """Initialize the document classifier."""
        self.categories = settings.DOCUMENT_CATEGORIES
    
    def classify(self, file_name: str, mime_type: str = "", content: str = "") -> str:
        """
        Classify a document based on file name, type, and content.
        
        Args:
            file_name: Name of the document file.
            mime_type: MIME type of the document.
            content: Text content of the document (optional).
        
        Returns:
            Category of the document (essay, transcript, letter_of_recommendation, other).
        """
        # Normalize file name
        file_name_lower = file_name.lower()
        content_lower = content.lower() if content else ""
        
        # Check each category
        for category, rules in self.categories.items():
            if category == "other":
                continue
            
            # Check file extension
            file_ext = os.path.splitext(file_name_lower)[0]
            for ext in rules.get("extensions", []):
                if file_name_lower.endswith(ext):
                    # Check keywords for confirmation
                    for keyword in rules.get("keywords", []):
                        if keyword in file_name_lower or keyword in content_lower:
                            logger.info(f"Classified '{file_name}' as {category}")
                            return category
            
            # Check keywords even if extension doesn't match
            for keyword in rules.get("keywords", []):
                if keyword in file_name_lower or keyword in content_lower:
                    logger.info(f"Classified '{file_name}' as {category} based on keywords")
                    return category
        
        logger.warning(f"Could not classify '{file_name}' - defaulting to 'other'")
        return "other"
    
    def classify_by_ai(self, file_name: str, content: str) -> Dict[str, any]:
        """
        Classify document using AI (requires OpenAI API).
        
        Args:
            file_name: Name of the document.
            content: Text content of the document.
        
        Returns:
            Dictionary with category and confidence score.
        """
        try:
            import openai
            
            if not settings.OPENAI_API_KEY:
                logger.warning("OPENAI_API_KEY not configured. Using rule-based classification.")
                return {"category": self.classify(file_name, content=content), "confidence": 0.5}
            
            openai.api_key = settings.OPENAI_API_KEY
            
            prompt = f"""Classify the following document into one of these categories:
- essay: Student's personal statement or essay
- transcript: Academic transcript or academic record
- letter_of_recommendation: Letter of recommendation from a professor or mentor
- other: Any other document type

Document name: {file_name}
Document preview: {content[:500]}...

Respond with ONLY the category name and a confidence score (0-1) in this format:
category: <category>
confidence: <score>"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=50
            )
            
            result_text = response["choices"][0]["message"]["content"].strip()
            lines = result_text.split("\n")
            
            category = "other"
            confidence = 0.5
            
            for line in lines:
                if line.startswith("category:"):
                    category = line.split(":", 1)[1].strip()
                elif line.startswith("confidence:"):
                    try:
                        confidence = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass
            
            logger.info(f"AI classified '{file_name}' as {category} (confidence: {confidence})")
            return {"category": category, "confidence": confidence}
        
        except Exception as e:
            logger.error(f"Error in AI classification: {e}")
            # Fall back to rule-based classification
            return {"category": self.classify(file_name, content=content), "confidence": 0.5}
