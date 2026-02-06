import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validator import DataValidator

def test_missing_values():
    """Test detection of missing values"""
    df = pd.DataFrame({
        'A': [1, 2, None, 4],
        'B': ['a', 'b', 'c', 'd']
    })
    
    validator = DataValidator(df)
    validator.check_missing_values()
    
    assert 'A' in validator.issues['missing_values']
    assert validator.issues['missing_values']['A']['count'] == 1
    assert 'B' not in validator.issues['missing_values']

def test_duplicates():
    """Test detection of duplicate rows"""
    df = pd.DataFrame({
        'A': [1, 2, 2, 3],
        'B': ['a', 'b', 'b', 'c']
    })
    
    validator = DataValidator(df)
    validator.check_duplicates()
    
    assert len(validator.issues['duplicates']) == 2

def test_email_validation():
    """Test email format validation"""
    df = pd.DataFrame({
        'email': ['valid@email.com', 'invalid_email', 'another@valid.com']
    })
    
    validator = DataValidator(df)
    validator.check_email_format()
    
    assert 'email' in validator.issues['format_errors']
    assert len(validator.issues['format_errors']['email']) == 1

def test_column_name_issues():
    """Test detection of problematic column names"""
    df = pd.DataFrame({
        'good_name': [1, 2, 3],
        'bad name': [4, 5, 6],
        'bad-name': [7, 8, 9]
    })
    
    validator = DataValidator(df)
    validator.check_column_names()
    
    assert len(validator.issues['column_name_issues']) == 2

if __name__ == "__main__":
    pytest.main([__file__, '-v'])