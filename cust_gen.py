# customer_data_generator.py

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

def generate_customer_data(num_customers=10, num_days=5):
    fake = Faker()

    data = {
        'CustomerID': [],
        'Name': [],
        'Email': [],
        'EntryDate': [],
        'FrequencyOfEntry': [],
        'ProductID': [],
        'PurchaseAmount': [],
        'Age': [],
        'Gender': [],
        'Category1': [],
        'Category2': [],
        'TotalItems': [],
        'DiscountPercentage': [],
        'TotalSpent': []
    }

    try:
        for customer_id in range(1, num_customers + 1):
            entry_dates = [datetime.now() - timedelta(days=np.random.randint(num_days)) for _ in range(np.random.randint(1, 6))]
            frequencies = [len(entry_dates)] * len(entry_dates)

            # Extend customer-specific information
            data['CustomerID'].extend([customer_id] * len(entry_dates))
            data['Name'].extend([fake.name()] * len(entry_dates))
            data['Email'].extend([fake.email()] * len(entry_dates))
            data['EntryDate'].extend(entry_dates)
            data['FrequencyOfEntry'].extend(frequencies)

            # Simulate customer purchases
            for date, frequency in zip(entry_dates, frequencies):
                products_purchased = np.random.choice(['A', 'B', 'C'], frequency)
                purchase_amounts = np.random.randint(10, 100, frequency)
                ages = np.random.randint(18, 65, frequency)
                genders = np.random.choice(['Male', 'Female'], frequency)
                category1 = np.random.choice(['X', 'Y', 'Z'], frequency)
                category2 = np.random.choice(['P', 'Q', 'R'], frequency)
                total_items = np.random.randint(1, 10, frequency)
                discount_percentage = np.random.uniform(0, 0.3, frequency)
                total_spent = np.random.uniform(50, 200, frequency)

                data['ProductID'].extend(products_purchased)
                data['PurchaseAmount'].extend(purchase_amounts)
                data['Age'].extend(ages)
                data['Gender'].extend(genders)
                data['Category1'].extend(category1)
                data['Category2'].extend(category2)
                data['TotalItems'].extend(total_items)
                data['DiscountPercentage'].extend(discount_percentage)
                data['TotalSpent'].extend(total_spent)

        # Ensure all arrays have the same length
        min_length = min(map(len, data.values()))
        for key in data:
            data[key] = data[key][:min_length]

        # Print lengths of arrays before creating DataFrame
        for key, value in data.items():
            print(f"Length of {key}: {len(value)}")

        customer_data = pd.DataFrame(data)
        customer_data.to_excel('customer_data.xlsx', index=False)
        print("Excel file generated successfully.")

    except ValueError as e:
        print(f"Error: {e}")
        print("Continuing with generating the Excel file...")

if __name__ == '__main__':
    generate_customer_data(num_customers=100, num_days=10)
