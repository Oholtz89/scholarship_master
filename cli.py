"""Simple CLI for running reports and queries."""
import argparse
import sys
from src.utils.report_generator import print_summary_report
from src.services import DatabaseService

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scholarship Master - CLI for reports and queries"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate reports")
    report_parser.add_argument(
        "type",
        choices=["summary", "category", "applicants"],
        help="Type of report to generate"
    )
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query submissions")
    query_parser.add_argument(
        "type",
        choices=["all", "pending", "completed", "error"],
        help="Type of submissions to query"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "report":
            if args.type == "summary":
                print_summary_report()
            else:
                print(f"Report type '{args.type}' not yet implemented")
        
        elif args.command == "query":
            db_service = DatabaseService()
            
            if args.type == "all":
                submissions = db_service.list_submissions()
            else:
                submissions = db_service.list_submissions(status=args.type)
            
            print(f"\nFound {len(submissions)} submissions:")
            for sub in submissions:
                print(f"  - {sub.applicant_name} ({sub.applicant_email}) - Status: {sub.status}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
