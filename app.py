from flask import Flask, render_template, request
import subprocess
import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
from collections import defaultdict

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Print Excel Data
@app.route('/print_excel_data')
def print_excel_data():
    # Add logic to read and return the Excel data as HTML (similar to your original logic)
    return "Print Excel Data"

# Form to Add Customer Data
@app.route('/add_customer_data')
def add_customer_data_form():
    return render_template('add_customer_data.html')

# Receive and Append New Customer Data
@app.route('/add_customer_data', methods=['POST'])
def add_customer_data():
    # Add logic to receive and append new customer data (similar to your original logic)
    return "Customer data added successfully!"
@app.route('/send_marketing_emails')
def send_marketing_emails():
    # Load the data from the Excel file
    file_path = 'customer_data.xlsx'
    df = pd.read_excel(file_path)

    # Define the Surprise reader
    reader = Reader(rating_scale=(df['PurchaseAmount'].min(), df['PurchaseAmount'].max()))

    # Load the data into the Surprise Dataset
    data = Dataset.load_from_df(df[['CustomerID', 'ProductID', 'PurchaseAmount']], reader)

    # Split the data into train and test sets
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    # Train the SVD model
    model = SVD(n_factors=50, random_state=42)
    model.fit(trainset)

    # Make predictions on the test set
    predictions = model.test(testset)

    # Create a dictionary to store the top N recommendations for each user
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Sort the predictions for each user and get the top 3
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:3]

    # Function to get product details from DataFrame based on ProductID
    def get_product_details(product_id):
        product_details = df[df['ProductID'] == product_id].iloc[0]
        return product_details[['ProductID', 'PurchaseAmount', 'Category1', 'Category2']]

    # Get the top 5 customers based on total spending
    top_5_customers = df.groupby('CustomerID')['TotalSpent'].sum().nlargest(5).index

    # Initialize a list to store customer results
    customer_results = []

    # Draft and print emails for the top 5 customers
    for customer_id in top_5_customers:
        # Initialize dictionaries to store customer details
        customer_result = {
            'email_details': [],
            'recommendations_details': [],
            'marketing_messages_details': [],
            'email_drafts': [],
            'evaluation_metrics': {}
        }

        customer_result['email_details'].append(f"\nSending email to Customer {customer_id}:")

        # Get customer details
        customer_details = df[df['CustomerID'] == customer_id].iloc[0]

        # Print customer details
        customer_result['email_details'].append(f"Customer Details: {customer_details[['CustomerID', 'Name', 'Email']]}")

        # Get top 3 recommendations for the customer
        recommendations = top_n[customer_id]

        # Print recommendations
        customer_result['recommendations_details'].append("\nTop 3 Recommendations:")
        for product_id, estimated_rating in recommendations:
            product_details = get_product_details(product_id)
            customer_result['recommendations_details'].append(
                f"ProductID: {product_details['ProductID']}, PurchaseAmount: {product_details['PurchaseAmount']}, "
                f"Category1: {product_details['Category1']}, Category2: {product_details['Category2']}, "
                f"Estimated Rating: {estimated_rating}")

        # Choose a random marketing message
        marketing_messages = {
            'A': 'Enjoy our premium product with a special discount!',
            'B': 'Discover our latest collection with an exclusive offer!',
            'C': 'Treat yourself with our best-selling item at a great price!',
        }

        # Print marketing message
        chosen_message = marketing_messages.get(product_details['Category1'], 'Discover our new products!')
        customer_result['marketing_messages_details'].append(f"\nMarketing Message: {chosen_message}")

        # Generate and print email draft
        email_draft = f"Subject: Special Offers Just for You!\n\nDear {customer_details['Name']},\n\n" \
                      f"We hope this email finds you well. As one of our valued customers, we have some special " \
                      f"recommendations for you:\n\n"

        for product_id, _ in recommendations:
            product_details = get_product_details(product_id)
            email_draft += f"- ProductID: {product_details['ProductID']}, PurchaseAmount: {product_details['PurchaseAmount']}, " \
                           f"Category1: {product_details['Category1']}, Category2: {product_details['Category2']}\n"

        email_draft += f"\n{chosen_message}\n\n" \
                       f"To show our appreciation, here's a coupon code: SPECIAL10\n" \
                       f"Use this code to enjoy exclusive discounts on these products. Happy shopping!\n\n" \
                       f"Best regards,\nThe Marketing Team"

        customer_result['email_drafts'].append("\nEmail Draft:\n")
        customer_result['email_drafts'].append(email_draft)

        # Evaluate the model and capture standard values
        evaluation_metrics = evaluate_model(model, testset)
        customer_result['evaluation_metrics'] = evaluation_metrics

        # Add the customer result to the list
        customer_results.append(customer_result)

    return render_template('result_mail.html', customer_results=customer_results)



# Evaluate Model Metrics
@app.route('/evaluate_model')
def evaluate_model():
    # Add logic to evaluate model metrics (similar to your original logic)
    return "Model Evaluated!"

if __name__ == '__main__':
    app.run(debug=True)

def evaluate_model(model, testset):
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)
    # Interpretation of metrics
    interpretation = "\nInterpretation:\n" \
                         "RMSE and MAE are standard metrics for evaluating prediction accuracy.\n" \
                         "Lower values indicate better accuracy. Comparing with the scale of PurchaseAmount can provide context.\n" \
                         "Here is a rough guide:\n" \
                         "   - RMSE < 10% of the PurchaseAmount range: Good\n" \
                         "   - RMSE ~ 20% of the PurchaseAmount range: Acceptable\n" \
                         "   - RMSE > 30% of the PurchaseAmount range: Needs improvement\n" \
                         f"\n   - MAE < 10% of the PurchaseAmount range: Good\n" \
                         f"   - MAE ~ 20% of the PurchaseAmount range: Acceptable\n" \
                         f"   - MAE > 30% of the PurchaseAmount range: Needs improvement"

    return {
            'RMSE': rmse,
            'MAE': mae,
            'Interpretation': interpretation
        }
