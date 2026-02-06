import pandas as pd
import sys
from pathlib import Path
from validator import DataValidator
from cleaner import DataCleaner
from tableau_prep import TableauPrep
from report_generator import ReportGenerator

def main():
    print("=" * 70)
    print("CSV DATA VALIDATOR AND CLEANER - TABLEAU EDITION")
    print("=" * 70)
    print()
    
    # Load data
    input_file = input("Enter CSV file path (or press Enter for sample): ").strip()
    if not input_file:
        input_file = "sample_data/sales_data.csv"
    
    try:
        df = pd.read_csv(input_file)
        print(f"\n[OK] Loaded {len(df)} rows and {len(df.columns)} columns from {input_file}")
    except FileNotFoundError:
        print(f"✗ Error: File '{input_file}' not found")
        return
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return
    
    # Validate
    print("\n" + "-" * 70)
    print("RUNNING VALIDATION CHECKS...")
    print("-" * 70)
    validator = DataValidator(df)
    issues = validator.validate_all()
    summary = validator.get_summary()
    
    # Display summary
    print("\nVALIDATION SUMMARY:")
    print(f"  • Column name issues: {summary['column_name_issues']}")
    print(f"  • Missing values in {summary['missing_values']} columns")
    print(f"  • {summary['duplicate_rows']} duplicate rows")
    print(f"  • Outliers in {summary['columns_with_outliers']} columns")
    print(f"  • Format errors in {summary['format_errors']} columns")
    print(f"  • Type errors in {summary['type_errors']} columns")
    
    # Track logs
    cleaning_log = None
    tableau_log = None
    
    # Ask about cleaning
    print("\n" + "-" * 70)
    print("Do you want to clean the data? (y/n): ", end='')
    if input().lower() == 'y':
        cleaner = DataCleaner(df)
        
        # Remove duplicates
        cleaner.remove_duplicates()
        
        # Auto-generate fill strategy
        strategy = {}
        for column in issues['missing_values'].keys():
            if df[column].dtype in ['int64', 'float64']:
                strategy[column] = 'median'
            else:
                strategy[column] = 'Unknown'
        
        if strategy:
            cleaner.fill_missing_values(strategy)
        
        # Remove outliers
        for column in issues['outliers'].keys():
            cleaner.remove_outliers(column, threshold=3.0)
        
        cleaned_df = cleaner.df
        cleaning_log = cleaner.get_cleaning_log()
        
        print(f"\n[OK] Data cleaned: {len(df)} rows → {len(cleaned_df)} rows (removed {len(df) - len(cleaned_df)})")
    else:
        cleaned_df = df
    
    # Tableau preparation
    print("\n" + "-" * 70)
    print("Prepare data for Tableau? (y/n): ", end='')
    if input().lower() == 'y':
        print("\nPREPARING DATA FOR TABLEAU...")
        tableau_prep = TableauPrep(cleaned_df)
        
        # Clean column names
        tableau_prep.clean_column_names()
        
        # Enforce data types
        tableau_prep.enforce_data_types()
        
        tableau_df = tableau_prep.df
        tableau_log = tableau_prep.get_prep_log()
        
        # Get dimension/measure suggestions
        suggestions = tableau_prep.create_dimension_measure_guide()
        
        # Generate metadata
        metadata_df = tableau_prep.generate_metadata()
        
        # Save files
        base_name = Path(input_file).stem
        output_dir = Path(input_file).parent
        
        tableau_file = output_dir / f"{base_name}_tableau_ready.csv"
        metadata_file = output_dir / f"{base_name}_metadata.csv"
        
        tableau_df.to_csv(tableau_file, index=False)
        metadata_df.to_csv(metadata_file, index=False)
        
        print(f"\n[OK] Tableau-ready data saved to: {tableau_file}")
        print(f"[OK] Metadata saved to: {metadata_file}")
        
        # Display Tableau suggestions
        print("\n" + "-" * 70)
        print("TABLEAU FIELD SUGGESTIONS:")
        print("-" * 70)
        if suggestions['dates']:
            print(f"\nDate Fields ({len(suggestions['dates'])}):")
            print(f"  {', '.join(suggestions['dates'])}")
        if suggestions['dimensions']:
            print(f"\nDimensions ({len(suggestions['dimensions'])}):")
            print(f"  {', '.join(suggestions['dimensions'])}")
        if suggestions['measures']:
            print(f"\nMeasures ({len(suggestions['measures'])}):")
            print(f"  {', '.join(suggestions['measures'])}")
        
        final_df = tableau_df
    else:
        final_df = cleaned_df
        print("\nSkipping Tableau preparation")
    
    # Save cleaned data (if not already saved as Tableau version)
    if cleaning_log and 'tableau_file' not in locals():
        output_file = input_file.replace('.csv', '_cleaned.csv')
        final_df.to_csv(output_file, index=False)
        print(f"\n[OK] Cleaned data saved to: {output_file}")

    
    # Generate report
    print("\n" + "-" * 70)
    Path("reports").mkdir(exist_ok=True)
    report_file = f"reports/validation_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    report = ReportGenerator.generate_text_report(
        issues, summary, cleaning_log, tableau_log, report_file
    )
    
    print("\nFULL VALIDATION REPORT:")
    print(report)
    
    print("\n" + "=" * 70)
    print("PROCESS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()