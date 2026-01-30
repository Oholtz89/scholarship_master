"""AI agent for grading documents based on scoring rubrics."""
import logging
from typing import Dict, Optional
import openai

from src.config import settings

logger = logging.getLogger(__name__)


class GradingAgent:
    """Agent for grading scholarship documents."""
    
    def __init__(self):
        """Initialize the grading agent."""
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        self.rubrics = settings.SCORING_RUBRIC
    
    def grade_document(self, category: str, content: str, file_name: str = "") -> Dict:
        """
        Grade a document based on its category and content.
        
        Args:
            category: Document category (essay, transcript, letter_of_recommendation).
            content: Text content of the document.
            file_name: Name of the document.
        
        Returns:
            Dictionary with scores and feedback.
        """
        if category not in self.rubrics:
            logger.warning(f"No rubric found for category: {category}")
            return {
                "category": category,
                "total_score": 0,
                "max_score": 100,
                "criteria_scores": {},
                "feedback": "No scoring rubric available for this document type.",
            }
        
        rubric = self.rubrics[category]
        
        try:
            if settings.OPENAI_API_KEY:
                return self._grade_with_ai(category, content, file_name, rubric)
            else:
                logger.info("OpenAI not configured. Using rule-based grading.")
                return self._grade_with_rules(category, content, rubric)
        except Exception as e:
            logger.error(f"Error grading document: {e}")
            return {
                "category": category,
                "total_score": 0,
                "max_score": rubric["max_score"],
                "criteria_scores": {},
                "feedback": f"Error during grading: {str(e)}",
            }
    
    def _grade_with_ai(self, category: str, content: str, file_name: str, rubric: Dict) -> Dict:
        """Grade using OpenAI API."""
        criteria = rubric.get("criteria", {})
        criteria_str = "\n".join([f"- {k}: {v}" for k, v in criteria.items()])
        
        prompt = f"""You are an expert scholarship evaluator. Grade the following {category} document.

Scoring Criteria:
{criteria_str}

Document Name: {file_name}
Content Preview:
{content[:2000]}...

Provide your grading in this exact format:
SCORE: <numeric score out of {rubric['max_score']}>
CRITERIA_SCORES:
<criteria_name>: <score>
<criteria_name>: <score>
FEEDBACK: <detailed feedback>

Be objective and thorough in your evaluation."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        
        result = response["choices"][0]["message"]["content"].strip()
        return self._parse_grading_response(category, result, rubric)
    
    def _grade_with_rules(self, category: str, content: str, rubric: Dict) -> Dict:
        """Grade using rule-based approach without AI."""
        # Simple rule-based scoring
        criteria_scores = {}
        max_score = rubric["max_score"]
        
        for criterion, config in rubric.get("criteria", {}).items():
            # Base score for presence
            score = config["max"] * 0.5
            
            # Bonus for content length and quality indicators
            if len(content) > 500:
                score += config["max"] * 0.25
            if any(word in content.lower() for word in ["quality", "excellent", "professional", "demonstrated"]):
                score += config["max"] * 0.15
            
            criteria_scores[criterion] = min(score, config["max"])
        
        total_score = sum(criteria_scores.values())
        
        return {
            "category": category,
            "total_score": total_score,
            "max_score": max_score,
            "criteria_scores": criteria_scores,
            "feedback": f"Rule-based grading: Document length {len(content)} characters. " +
                       f"Estimated {category} quality based on content analysis.",
        }
    
    def _parse_grading_response(self, category: str, response: str, rubric: Dict) -> Dict:
        """Parse AI grading response."""
        lines = response.split("\n")
        total_score = 0
        criteria_scores = {}
        feedback = ""
        
        parsing_feedback = False
        for line in lines:
            line = line.strip()
            
            if line.startswith("SCORE:"):
                try:
                    total_score = float(line.split(":", 1)[1].strip())
                except ValueError:
                    pass
            
            elif line.startswith("CRITERIA_SCORES:"):
                parsing_feedback = False
            
            elif line.startswith("FEEDBACK:"):
                feedback = line.split(":", 1)[1].strip()
                parsing_feedback = True
            
            elif ":" in line and not line.startswith("SCORE") and not line.startswith("CRITERIA"):
                # Parse criteria scores
                parts = line.split(":", 1)
                if len(parts) == 2:
                    try:
                        criterion = parts[0].strip().lower()
                        score = float(parts[1].strip())
                        if criterion in rubric.get("criteria", {}):
                            criteria_scores[criterion] = score
                    except ValueError:
                        pass
            
            elif parsing_feedback and line:
                feedback += " " + line
        
        return {
            "category": category,
            "total_score": min(total_score, rubric["max_score"]),
            "max_score": rubric["max_score"],
            "criteria_scores": criteria_scores,
            "feedback": feedback.strip(),
        }
