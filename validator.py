import pandas as pd
import numpy as np
from typing import Dict, List, Any
import re

class DataValidator:
    """Validates CSV data and identifies quality issues"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.issues = {
            'missing_values': {},
            'duplicates': [],
            'type_errors': {},
            'outliers': {},
            'format_errors': {},
            'column_name_issues': []
        }
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks"""
        self.check_column_names()
        self.check_missing_values()
        self.check_duplicates()
        self.check_numeric_outliers()
        self.check_email_format()
        self.check_date_format()
        self.check_boolean_consistency()
        return self.issues
    
    def check_column_names(self):
        """Check for problematic column names (for Tableau compatibility)"""
        issues = []
        for column in self.df.columns:
            problems = []
            
            # Check for spaces
            if ' ' in column:
                problems.append('contains spaces')
            
            # Check for special characters
            if re.search(r'[^a-zA-Z0-9_]', column.replace(' ', '')):
                problems.append('contains special characters')
            
            # Check for inconsistent casing
            if column != column.lower() and column != column.upper() and column != column.title():
                problems.append('inconsistent casing')
            
            if problems:
                issues.append({
                    'column': column,
                    'problems': problems
                })
        
        if issues:
            self.issues['column_name_issues'] = issues
    
    def check_missing_values(self):
        """Identify missing values in each column"""
        for column in self.df.columns:
            null_count = self.df[column].isnull().sum()
            if null_count > 0:
                self.issues['missing_values'][column] = {
                    'count': int(null_count),
                    'percentage': round((null_count / len(self.df)) * 100, 2)
                }
    
    def check_duplicates(self):
        """Find duplicate rows"""
        duplicates = self.df[self.df.duplicated(keep=False)]
        if len(duplicates) > 0:
            self.issues['duplicates'] = duplicates.to_dict('records')
    
    def check_numeric_outliers(self, threshold: float = 3.0):
        """Detect outliers in numeric columns using z-score"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_cols:
            # Skip if column has too many missing values
            if self.df[column].isnull().sum() > len(self.df) * 0.5:
                continue
                
            mean = self.df[column].mean()
            std = self.df[column].std()
            
            if std == 0:  # Avoid division by zero
                continue
            
            z_scores = np.abs((self.df[column] - mean) / std)
            outliers = self.df[z_scores > threshold]
            
            if len(outliers) > 0:
                self.issues['outliers'][column] = {
                    'count': len(outliers),
                    'values': outliers[column].tolist(),
                    'indices': outliers.index.tolist()
                }
    
    def check_email_format(self):
        """Validate email format in columns containing 'email'"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for column in self.df.columns:
            if 'email' in column.lower():
                invalid_emails = []
                for idx, value in self.df[column].items():
                    if pd.notna(value) and not re.match(email_pattern, str(value)):
                        invalid_emails.append({
                            'index': int(idx),
                            'value': str(value)
                        })
                
                if invalid_emails:
                    self.issues['format_errors'][column] = invalid_emails
    
    def check_date_format(self):
        """Validate date format in columns containing 'date'"""
        for column in self.df.columns:
            if 'date' in column.lower():
                invalid_dates = []
                for idx, value in self.df[column].items():
                    if pd.notna(value):
                        try:
                            pd.to_datetime(value)
                        except:
                            invalid_dates.append({
                                'index': int(idx),
                                'value': str(value)
                            })
                
                if invalid_dates:
                    if column not in self.issues['format_errors']:
                        self.issues['format_errors'][column] = []
                    self.issues['format_errors'][column].extend(invalid_dates)
    
    def check_boolean_consistency(self):
        """Check for inconsistent boolean values"""
        for column in self.df.columns:
            if self.df[column].dtype == 'object':
                unique_vals = set(self.df[column].dropna().astype(str).unique())
                bool_vals = {'True', 'False', 'true', 'false', '0', '1', 'yes', 'no', 'Yes', 'No'}
                
                if unique_vals.issubset(bool_vals) and len(unique_vals) >= 2:
                    self.issues['type_errors'][column] = {
                        'issue': 'Inconsistent boolean format',
                        'values': list(unique_vals)
                    }
    
    def get_summary(self) -> Dict[str, int]:
        """Get count of each issue type"""
        return {
            'missing_values': len(self.issues['missing_values']),
            'duplicate_rows': len(self.issues['duplicates']),
            'columns_with_outliers': len(self.issues['outliers']),
            'format_errors': len(self.issues['format_errors']),
            'column_name_issues': len(self.issues['column_name_issues']),
            'type_errors': len(self.issues['type_errors']),
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns)
        }