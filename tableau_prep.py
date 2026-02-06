import pandas as pd
import numpy as np
import re
from typing import Dict, List

class TableauPrep:
    """Prepare data specifically for Tableau visualization"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.prep_log = []
    
    def clean_column_names(self):
        """Standardize column names for Tableau"""
        new_columns = {}
        for col in self.df.columns:
            # Remove special characters except underscores
            clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', col)
            # Remove multiple consecutive underscores
            clean_name = re.sub(r'_+', '_', clean_name)
            # Strip leading/trailing underscores
            clean_name = clean_name.strip('_')
            # Convert to Title Case with underscores
            clean_name = '_'.join(word.capitalize() for word in clean_name.split('_'))
            
            new_columns[col] = clean_name
        
        self.df.rename(columns=new_columns, inplace=True)
        self.prep_log.append(f"Standardized {len(new_columns)} column names for Tableau")
        return self.df
    
    def enforce_data_types(self):
        """Ensure proper data types for Tableau"""
        type_changes = []
        
        for column in self.df.columns:
            original_type = str(self.df[column].dtype)
            
            # Convert date columns to datetime
            if 'date' in column.lower() and self.df[column].dtype == 'object':
                try:
                    self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
                    type_changes.append(f"{column}: {original_type} → datetime64")
                except:
                    pass
            
            # Convert boolean columns
            if self.df[column].dtype == 'object':
                unique_values = set(self.df[column].dropna().astype(str).unique())
                bool_vals = {'True', 'False', 'true', 'false', '0', '1', 'yes', 'no', 'Yes', 'No'}
                
                if unique_values.issubset(bool_vals):
                    bool_map = {
                        'True': True, 'true': True, '1': True, 'yes': True, 'Yes': True,
                        'False': False, 'false': False, '0': False, 'no': False, 'No': False
                    }
                    self.df[column] = self.df[column].map(bool_map)
                    type_changes.append(f"{column}: {original_type} → boolean")
            
            # Convert numeric strings to numbers
            if self.df[column].dtype == 'object':
                try:
                    # Try to convert to numeric
                    numeric_col = pd.to_numeric(self.df[column], errors='coerce')
                    # Only convert if most values are successfully converted
                    if numeric_col.notna().sum() / len(self.df) > 0.8:
                        self.df[column] = numeric_col
                        type_changes.append(f"{column}: {original_type} → numeric")
                except:
                    pass
        
        if type_changes:
            self.prep_log.append(f"Converted {len(type_changes)} column types")
            for change in type_changes:
                self.prep_log.append(f"  - {change}")
        
        return self.df
    
    def create_dimension_measure_guide(self) -> Dict[str, List[str]]:
        """Suggest which columns should be dimensions vs measures in Tableau"""
        suggestions = {
            'dimensions': [],
            'measures': [],
            'dates': []
        }
        
        for column in self.df.columns:
            dtype = self.df[column].dtype
            unique_ratio = self.df[column].nunique() / len(self.df) if len(self.df) > 0 else 0
            
            # Date fields
            if pd.api.types.is_datetime64_any_dtype(dtype):
                suggestions['dates'].append(column)
            
            # Numeric columns
            elif dtype in ['int64', 'float64']:
                # High cardinality numeric = likely a measure
                if unique_ratio > 0.5:
                    suggestions['measures'].append(column)
                # Low cardinality numeric = likely a dimension (category codes, ratings, etc.)
                else:
                    suggestions['dimensions'].append(column)
            
            # Boolean and string columns = dimensions
            else:
                suggestions['dimensions'].append(column)
        
        return suggestions
    
    def generate_metadata(self) -> pd.DataFrame:
        """Create metadata DataFrame describing each column"""
        metadata = {
            'Column_Name': [],
            'Data_Type': [],
            'Null_Count': [],
            'Null_Percentage': [],
            'Unique_Values': [],
            'Sample_Values': [],
            'Min_Value': [],
            'Max_Value': [],
            'Suggested_Role': []
        }
        
        suggestions = self.create_dimension_measure_guide()
        
        for column in self.df.columns:
            metadata['Column_Name'].append(column)
            metadata['Data_Type'].append(str(self.df[column].dtype))
            
            # Null information
            null_count = self.df[column].isnull().sum()
            metadata['Null_Count'].append(int(null_count))
            metadata['Null_Percentage'].append(round((null_count / len(self.df)) * 100, 2))
            
            # Unique values
            metadata['Unique_Values'].append(int(self.df[column].nunique()))
            
            # Sample values
            samples = self.df[column].dropna().head(3).tolist()
            metadata['Sample_Values'].append(', '.join(str(x)[:50] for x in samples))
            
            # Min/Max for numeric columns
            if self.df[column].dtype in ['int64', 'float64']:
                metadata['Min_Value'].append(self.df[column].min())
                metadata['Max_Value'].append(self.df[column].max())
            else:
                metadata['Min_Value'].append('N/A')
                metadata['Max_Value'].append('N/A')
            
            # Suggested role in Tableau
            if column in suggestions['dimensions']:
                role = 'Dimension'
            elif column in suggestions['measures']:
                role = 'Measure'
            elif column in suggestions['dates']:
                role = 'Date'
            else:
                role = 'Unknown'
            metadata['Suggested_Role'].append(role)
        
        return pd.DataFrame(metadata)
    
    def get_prep_log(self) -> List[str]:
        """Return log of all prep operations"""
        return self.prep_log