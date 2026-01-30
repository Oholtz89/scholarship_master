"""Tests for the scholarship submission workflow."""
import unittest
from unittest.mock import Mock, patch
from src.services.document_classifier import DocumentClassifier
from src.services.grading_agent import GradingAgent


class TestDocumentClassifier(unittest.TestCase):
    """Test document classification."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.classifier = DocumentClassifier()
    
    def test_classify_essay(self):
        """Test classifying an essay."""
        result = self.classifier.classify(
            "Personal_Essay.pdf",
            mime_type="application/pdf",
            content="This essay discusses my personal journey..."
        )
        self.assertEqual(result, "essay")
    
    def test_classify_transcript(self):
        """Test classifying a transcript."""
        result = self.classifier.classify(
            "Academic_Transcript.pdf",
            mime_type="application/pdf",
            content="GPA: 3.9, Academic Record"
        )
        self.assertEqual(result, "transcript")
    
    def test_classify_letter_of_recommendation(self):
        """Test classifying a letter of recommendation."""
        result = self.classifier.classify(
            "Letter_of_Recommendation.pdf",
            mime_type="application/pdf",
            content="This letter of recommendation is for..."
        )
        self.assertEqual(result, "letter_of_recommendation")
    
    def test_classify_unknown_category(self):
        """Test classifying unknown document type."""
        result = self.classifier.classify(
            "random_file.txt",
            mime_type="text/plain",
            content="Some random content"
        )
        self.assertEqual(result, "other")


class TestGradingAgent(unittest.TestCase):
    """Test document grading."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.grading_agent = GradingAgent()
    
    def test_grade_essay(self):
        """Test grading an essay."""
        content = """
        This essay explores the concept of leadership and personal growth.
        Throughout my high school career, I have developed strong leadership skills
        through various experiences in student government and community service.
        I believe that effective leadership requires empathy, clear communication,
        and a commitment to serving others. This experience has shaped my desire
        to pursue a career in public service.
        """
        
        result = self.grading_agent.grade_document(
            "essay",
            content,
            "my_essay.pdf"
        )
        
        self.assertIn("total_score", result)
        self.assertIn("max_score", result)
        self.assertIn("criteria_scores", result)
        self.assertEqual(result["category"], "essay")
    
    def test_grade_invalid_category(self):
        """Test grading with invalid category."""
        result = self.grading_agent.grade_document(
            "invalid_category",
            "Some content",
            "file.pdf"
        )
        
        self.assertEqual(result["total_score"], 0)
        self.assertIn("No scoring rubric", result["feedback"])


if __name__ == "__main__":
    unittest.main()
