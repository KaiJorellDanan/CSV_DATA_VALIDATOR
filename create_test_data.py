import pandas as pd
import numpy as np

# Create sample sales data with intentional issues for validation
data = {
    'order id': [1, 2, 3, 4, 5, 5, 7, 8, 9, 10, 11, 12],  # Duplicate ID 5, space in name
    'customer name': ['John Doe', 'Jane Smith', None, 'Bob Johnson', 'Alice Williams', 
                      'Alice Williams', 'Charlie Brown', 'Diana Prince', 'Eve Davis', 
                      'Frank Miller', 'Grace Lee', 'Henry Wilson'],
    'customer-email': ['john@email.com', 'jane@email.com', 'invalid_email', 'bob@email.com',
                       'alice@email.com', 'alice@email.com', None, 'diana@email.com', 
                       'eve@email.com', 'frank@email.com', 'grace@email.com', 'henry@email.com'],
    'Age': [25, 30, -5, 45, 28, 28, 35, 150, 22, 40, 33, 29],  # -5 and 150 are outliers
    'order_amount': [100.50, 250.75, 50.00, None, 300.00, 300.00, 175.25, 
                     425.50, 80.00, 999999.99, 200.00, 150.50],  # Missing value and extreme outlier
    'order date': ['2024-01-15', '2024-01-16', '2024-13-45', '2024-01-18',
                   '2024-01-19', '2024-01-19', '2024-01-20', '2024-01-21',
                   '2024-01-22', '2024-01-23', '2024-01-24', '2024-01-25'],  # Invalid date
    'product_category': ['Electronics', 'Clothing', 'Electronics', 'Home', 'Electronics',
                        'Electronics', 'Clothing', 'Home', 'Electronics', 'Clothing',
                        'Home', 'Electronics'],
    'quantity': [1, 2, 1, 3, 1, 1, 2, 1, 1, 5, 2, 1],
    'is_shipped': ['True', 'False', 'True', 'True', 'False', 'False', 'True', 
                   'True', '1', '0', 'True', 'False']  # Mixed boolean formats
}

df = pd.DataFrame(data)
df.to_csv('sample_data/sales_data.csv', index=False)
print("Created sample_data/sales_data.csv")
print(f"  Rows: {len(df)}")
print(f"  Columns: {len(df.columns)}")
print("  Issues included: duplicates, missing values, outliers, format errors, inconsistent naming")