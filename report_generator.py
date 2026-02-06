import pandas as pd
from datetime import datetime
from typing import Dict, Any, List

class ReportGenerator:
    """Generate validation and cleaning reports"""
    
    @staticmethod
    def generate_text_report(issues: Dict[str, Any], summary: Dict[str, int], 
                            cleaning_log: List[str] = None, 
                            tableau_log: List[str] = None,
                            output_file: str = None):
        """Generate comprehensive text report"""
        
        report = []
        report.append("=" * 70)
        report.append("CSV DATA VALIDATOR AND CLEANER - TABLEAU EDITION")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        report.append("SUMMARY")
        report.append("-" * 70)
        for key, value in summary.items():
            report.append(f"{key.replace('_', ' ').title()}: {value}")
        report.append("")
        
        # Column Name Issues
        if issues.get('column_name_issues'):
            report.append("COLUMN NAME ISSUES (Tableau Compatibility)")
            report.append("-" * 70)
            for issue in issues['column_name_issues']:
                report.append(f"Column '{issue['column']}':")
                for problem in issue['problems']:
                    report.append(f"  - {problem}")
            report.append("")
        
        # Missing Values
        if issues['missing_values']:
            report.append("MISSING VALUES")
            report.append("-" * 70)
            for column, data in issues['missing_values'].items():
                report.append(f"Column '{column}': {data['count']} missing ({data['percentage']}%)")
            report.append("")
        
        # Duplicates
        if issues['duplicates']:
            report.append("DUPLICATE ROWS")
            report.append("-" * 70)
            report.append(f"Found {len(issues['duplicates'])} duplicate rows")
            report.append("")
        
        # Outliers
        if issues['outliers']:
            report.append("OUTLIERS DETECTED")
            report.append("-" * 70)
            for column, data in issues['outliers'].items():
                report.append(f"Column '{column}': {data['count']} outliers")
                report.append(f"  Values: {data['values']}")
            report.append("")
        
        # Format Errors
        if issues['format_errors']:
            report.append("FORMAT ERRORS")
            report.append("-" * 70)
            for column, errors in issues['format_errors'].items():
                report.append(f"Column '{column}': {len(errors)} format errors")
                for error in errors[:5]:
                    report.append(f"  Row {error['index']}: '{error['value']}'")
                if len(errors) > 5:
                    report.append(f"  ... and {len(errors) - 5} more")
            report.append("")
        
        # Type Errors
        if issues.get('type_errors'):
            report.append("DATA TYPE ISSUES")
            report.append("-" * 70)
            for column, data in issues['type_errors'].items():
                report.append(f"Column '{column}': {data['issue']}")
                report.append(f"  Found values: {data['values']}")
            report.append("")
        
        # Cleaning Log
        if cleaning_log:
            report.append("CLEANING OPERATIONS")
            report.append("-" * 70)
            for log_entry in cleaning_log:
                report.append(f"✓ {log_entry}")
            report.append("")
        
        # Tableau Prep Log
        if tableau_log:
            report.append("TABLEAU PREPARATION")
            report.append("-" * 70)
            for log_entry in tableau_log:
                report.append(f"✓ {log_entry}")
            report.append("")
        
        report.append("=" * 70)
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:  # Added encoding='utf-8'
                f.write(report_text)
            print(f"\nReport saved to: {output_file}")
        
        return report_text