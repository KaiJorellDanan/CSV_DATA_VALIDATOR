# CSV Data Validator and Cleaner - Tableau Edition

Automated data quality tool for cleaning CSV files and preparing them for Tableau visualization. Detects data issues, cleans problematic records, and optimizes column formats for BI tools.

## Features

### Data Validation
- Missing value detection with statistics
- Duplicate row identification
- Outlier detection using z-score analysis
- Email and date format validation
- Boolean value consistency checks
- Column naming issues (spaces, special characters)

### Data Cleaning
- Automated duplicate removal
- Configurable missing value imputation (mean, median, mode, custom values)
- Outlier removal based on statistical thresholds
- Invalid value correction

### Tableau Preparation
- Column name standardization (remove spaces, special characters)
- Data type enforcement (datetime, boolean, numeric conversion)
- Dimension vs Measure classification suggestions
- Metadata generation for data dictionary
- Tableau-optimized CSV export

## Installation
```bash
# Clone repository
git clone <your-repo-url>
cd csv-data-validator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
python src/main.py
```

Follow the interactive prompts to:
1. Select CSV file to validate
2. Review validation results
3. Clean data automatically
4. Prepare for Tableau
5. Export cleaned data and metadata

### Programmatic Usage
```python
import pandas as pd
from src.validator import DataValidator
from src.cleaner import DataCleaner
from src.tableau_prep import TableauPrep

# Load data
df = pd.read_csv('your_data.csv')

# Validate
validator = DataValidator(df)
issues = validator.validate_all()

# Clean
cleaner = DataCleaner(df)
cleaner.remove_duplicates()
cleaner.fill_missing_values({'age': 'median', 'name': 'Unknown'})
cleaned_df = cleaner.df

# Prepare for Tableau
tableau_prep = TableauPrep(cleaned_df)
tableau_prep.clean_column_names()
tableau_prep.enforce_data_types()
tableau_ready_df = tableau_prep.df

# Get field suggestions
suggestions = tableau_prep.create_dimension_measure_guide()
print(f"Dimensions: {suggestions['dimensions']}")
print(f"Measures: {suggestions['measures']}")
```

## Tableau Workflow

1. Run validator on raw CSV
2. Review validation report
3. Clean data with automated strategies
4. Prepare for Tableau (standardize names, types)
5. Export `*_tableau_ready.csv` and `*_metadata.csv`
6. Load cleaned CSV into Tableau
7. Reference metadata for field descriptions
8. Use dimension/measure suggestions for initial visualizations

## Example Output
```
VALIDATION SUMMARY:
  • Column name issues: 3
  • Missing values in 2 columns
  • 2 duplicate rows
  • Outliers in 2 columns
  • Format errors in 1 columns

TABLEAU FIELD SUGGESTIONS:
  Date Fields: Order_Date
  Dimensions: Customer_Name, Product_Category, Is_Shipped
  Measures: Order_Amount, Quantity, Age
```

## Project Structure
```
csv-data-validator/
├── src/
│   ├── validator.py          # Data validation engine
│   ├── cleaner.py            # Data cleaning operations
│   ├── tableau_prep.py       # Tableau-specific preparation
│   ├── report_generator.py   # Report generation
│   └── main.py               # CLI interface
├── tests/
│   ├── test_validator.py     # Validation tests
│   └── test_tableau_prep.py  # Tableau prep tests
├── sample_data/              # Sample datasets
│   └── create_test_data.py   # Test data generator
├── reports/                  # Generated validation reports
├── requirements.txt
└── README.md
```

## Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_validator.py -v
```

## Technologies

- **Python 3.8+**
- **pandas** - data manipulation and analysis
- **numpy** - numerical computing and statistics
- **pytest** - testing framework

## Data Quality Checks

| Check | Description |
|-------|-------------|
| Missing Values | Identifies null/NaN values with percentages |
| Duplicates | Finds exact duplicate rows |
| Outliers | Detects statistical outliers (z-score > 3) |
| Email Format | Validates email addresses with regex |
| Date Format | Validates date strings and converts to datetime |
| Boolean Consistency | Identifies mixed boolean formats (True/1/yes) |
| Column Names | Flags spaces and special characters |

## Use Cases

- Cleaning messy CSV exports before Tableau analysis
- Standardizing data from multiple sources
- Automating data quality checks in ETL pipelines
- Preparing datasets for business intelligence tools
- Creating data dictionaries for analyst teams

## License

MIT License
