import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tableau_prep import TableauPrep

def test_clean_column_names():
    """Test column name standardization"""
    df = pd.DataFrame({
        'order id': [1, 2, 3],
        'customer-name': ['A', 'B', 'C'],
        'order_amount': [100, 200, 300]
    })
    
    prep = TableauPrep(df)
    prep.clean_column_names()
    
    assert 'Order_Id' in prep.df.columns
    assert 'Customer_Name' in prep.df.columns
    assert 'Order_Amount' in prep.df.columns

def test_dimension_measure_suggestions():
    """Test dimension vs measure classification"""
    df = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B'],
        'amount': [100, 200, 150, 250],
        'date': pd.date_range('2024-01-01', periods=4)
    })
    
    prep = TableauPrep(df)
    suggestions = prep.create_dimension_measure_guide()
    
    assert 'category' in suggestions['dimensions']
    assert 'amount' in suggestions['measures']
    assert 'date' in suggestions['dates']

if __name__ == "__main__":
    pytest.main([__file__, '-v'])