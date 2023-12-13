# sample_data_generator.py

import pandas as pd
import numpy as np

def generate_sample_data(num_samples=500):
    # Generate sample structured data for a supermarket dataset

    # Sample product names and corresponding categories
    products = {
        'A': {'name': 'Milk', 'category1': 'Dairy', 'category2': 'Liquid'},
        'B': {'name': 'Bread', 'category1': 'Bakery', 'category2': 'Loaf'},
        'C': {'name': 'Bananas', 'category1': 'Produce', 'category2': 'Fruit'},
        # Add more products with realistic names and categories
    }

    data = {
        'CustomerID': np.arange(1, num_samples + 1),
        'ProductID': np.random.choice(list(products.keys()), num_samples),
        'ProductName': [products[product]['name'] for product in np.random.choice(list(products.keys()), num_samples)],
        'Category1': [products[product]['category1'] for product in np.random.choice(list(products.keys()), num_samples)],
        'Category2': [products[product]['category2'] for product in np.random.choice(list(products.keys()), num_samples)],
        'PurchaseAmount': np.random.randint(1, 10, num_samples),
        'Age': np.random.randint(18, 65, num_samples),
        'Gender': np.random.choice(['Male', 'Female'], num_samples),
        'TotalItems': np.random.randint(1, 10, num_samples),
        'DiscountPercentage': np.random.uniform(0, 0.3, num_samples),
        'TotalSpent': np.random.uniform(50, 200, num_samples)
    }

    sample_data = pd.DataFrame(data)
    sample_data.to_excel('sample_data.xlsx', index=False)

if __name__ == '__main__':
    generate_sample_data(num_samples=500)
