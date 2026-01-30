"""Query and reporting utilities for scholarship submissions."""
import logging
from typing import List, Dict, Optional
from src.services import DatabaseService

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate reports from submission data."""
    
    def __init__(self):
        """Initialize report generator."""
        self.db_service = DatabaseService()
    
    def generate_summary_report(self) -> Dict:
        """Generate a summary report of all submissions."""
        submissions = self.db_service.list_submissions()
        
        total_submissions = len(submissions)
        completed = len([s for s in submissions if s.status == "completed"])
        processing = len([s for s in submissions if s.status == "processing"])
        errors = len([s for s in submissions if s.status == "error"])
        
        all_scores = []
        for submission in submissions:
            scores = self.db_service.get_submission_scores(submission.id)
            all_scores.extend(scores)
        
        avg_score = sum(s.total_score for s in all_scores) / len(all_scores) if all_scores else 0
        
        return {
            "total_submissions": total_submissions,
            "completed": completed,
            "processing": processing,
            "errors": errors,
            "total_documents": len([d for s in submissions for d in s.documents]),
            "average_score": avg_score,
            "high_score": max((s.total_score for s in all_scores), default=0),
            "low_score": min((s.total_score for s in all_scores), default=0),
        }
    
    def generate_category_report(self) -> Dict[str, Dict]:
        """Generate report by document category."""
        submissions = self.db_service.list_submissions()
        categories = {}
        
        for submission in submissions:
            scores = self.db_service.get_submission_scores(submission.id)
            for score in scores:
                if score.category not in categories:
                    categories[score.category] = {
                        "count": 0,
                        "total_score": 0,
                        "avg_score": 0,
                        "scores": []
                    }
                categories[score.category]["count"] += 1
                categories[score.category]["total_score"] += score.total_score
                categories[score.category]["scores"].append(score.total_score)
        
        for cat in categories:
            if categories[cat]["count"] > 0:
                categories[cat]["avg_score"] = categories[cat]["total_score"] / categories[cat]["count"]
        
        return categories
    
    def get_top_applicants(self, limit: int = 10) -> List[Dict]:
        """Get top scoring applicants."""
        submissions = self.db_service.list_submissions()
        
        applicants = []
        for submission in submissions:
            scores = self.db_service.get_submission_scores(submission.id)
            total_score = sum(s.total_score for s in scores)
            
            applicants.append({
                "applicant_name": submission.applicant_name,
                "applicant_email": submission.applicant_email,
                "total_score": total_score,
                "document_count": len(submission.documents),
                "status": submission.status,
            })
        
        # Sort by score descending
        applicants.sort(key=lambda x: x["total_score"], reverse=True)
        return applicants[:limit]


def print_summary_report():
    """Print a summary report to console."""
    generator = ReportGenerator()
    
    print("\n" + "=" * 80)
    print("SCHOLARSHIP SUBMISSION SUMMARY REPORT")
    print("=" * 80)
    
    summary = generator.generate_summary_report()
    print(f"\nTotal Submissions: {summary['total_submissions']}")
    print(f"  - Completed: {summary['completed']}")
    print(f"  - Processing: {summary['processing']}")
    print(f"  - Errors: {summary['errors']}")
    print(f"\nTotal Documents: {summary['total_documents']}")
    print(f"Average Score: {summary['average_score']:.2f}")
    print(f"Score Range: {summary['low_score']:.1f} - {summary['high_score']:.1f}")
    
    print("\n" + "-" * 80)
    print("SCORES BY CATEGORY")
    print("-" * 80)
    
    categories = generator.generate_category_report()
    for category, data in categories.items():
        print(f"\n{category.upper()}")
        print(f"  Count: {data['count']}")
        print(f"  Average Score: {data['avg_score']:.2f}")
        print(f"  Min/Max: {min(data['scores']):.1f} / {max(data['scores']):.1f}")
    
    print("\n" + "-" * 80)
    print("TOP APPLICANTS")
    print("-" * 80)
    
    top_applicants = generator.get_top_applicants(10)
    for i, applicant in enumerate(top_applicants, 1):
        print(f"{i}. {applicant['applicant_name']} ({applicant['applicant_email']})")
        print(f"   Score: {applicant['total_score']:.1f} | Documents: {applicant['document_count']} | Status: {applicant['status']}")
    
    print("\n" + "=" * 80)
