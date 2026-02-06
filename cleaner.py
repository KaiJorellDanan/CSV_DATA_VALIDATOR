import pandas as pd
import numpy as np
from typing import Dict, Any

class DataCleaner:
    """Cleans data based on validation results"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.cleaning_log = []
    
    def remove_duplicates(self, keep: str = 'first') -> pd.DataFrame:
        """Remove duplicate rows"""
        before_count = len(self.df)
        self.df = self.df.drop_duplicates(keep=keep)
        removed = before_count - len(self.df)
        
        if removed > 0:
            self.cleaning_log.append(f"Removed {removed} duplicate rows")
        
        return self.df
    
    def fill_missing_values(self, strategy: Dict[str, Any]):
        """
        Fill missing values based on strategy
        strategy example: {'age': 'mean', 'name': 'Unknown', 'email': 'drop'}
        """
        for column, method in strategy.items():
            if column not in self.df.columns:
                continue
            
            missing_count = self.df[column].isnull().sum()
            if missing_count == 0:
                continue
            
           # Find this section (around line 40-44) and replace:
            if method == 'mean':
                fill_value = self.df[column].mean()
                self.df[column] = self.df[column].fillna(fill_value)  # Changed from inplace
                self.cleaning_log.append(f"Filled {missing_count} missing values in '{column}' with mean: {fill_value:.2f}")
            
            elif method == 'median':
                fill_value = self.df[column].median()
                self.df[column] = self.df[column].fillna(fill_value)  # Changed from inplace
                self.cleaning_log.append(f"Filled {missing_count} missing values in '{column}' with median: {fill_value:.2f}")
            
            elif method == 'mode':
                fill_value = self.df[column].mode()[0] if not self.df[column].mode().empty else 'Unknown'
                self.df[column] = self.df[column].fillna(fill_value)  # Changed from inplace
                self.cleaning_log.append(f"Filled {missing_count} missing values in '{column}' with mode: {fill_value}")
            
            elif method == 'drop':
                before_count = len(self.df)
                self.df = self.df.dropna(subset=[column])
                removed = before_count - len(self.df)
                self.cleaning_log.append(f"Dropped {removed} rows with missing '{column}'")
            
            else:  # Treat as literal fill value
                self.df[column] = self.df[column].fillna(method)  # Changed from inplace
                self.cleaning_log.append(f"Filled {missing_count} missing values in '{column}' with '{method}'")
        
        return self.df
    
    def remove_outliers(self, column: str, threshold: float = 3.0):
        """Remove outliers from numeric column using z-score"""
        if column not in self.df.columns:
            return self.df
        
        before_count = len(self.df)
        mean = self.df[column].mean()
        std = self.df[column].std()
        
        if std == 0:
            return self.df
        
        z_scores = np.abs((self.df[column] - mean) / std)
        self.df = self.df[z_scores <= threshold]
        removed = before_count - len(self.df)
        
        if removed > 0:
            self.cleaning_log.append(f"Removed {removed} outliers from '{column}'")
        
        return self.df
    
    def fix_invalid_values(self, column: str, invalid_indices: list, fix_value: Any):
        """Replace invalid values at specific indices"""
        count = 0
        for idx in invalid_indices:
            if idx in self.df.index:
                self.df.at[idx, column] = fix_value
                count += 1
        
        if count > 0:
            self.cleaning_log.append(f"Fixed {count} invalid values in '{column}'")
        
        return self.df
    
    def get_cleaning_log(self) -> list:
        """Return log of all cleaning operations"""
        return self.cleaning_log