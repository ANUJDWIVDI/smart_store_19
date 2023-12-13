import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
from collections import defaultdict

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

# Sample marketing messages
marketing_messages = {
    'A': 'Enjoy our premium product with a special discount!',
    'B': 'Discover our latest collection with an exclusive offer!',
    'C': 'Treat yourself with our best-selling item at a great price!',
}

# Draft and print emails for the top 5 customers
for customer_id in top_5_customers:
    print(f"\nSending email to Customer {customer_id}:")

    # Get customer details
    customer_details = df[df['CustomerID'] == customer_id].iloc[0]

    # Print customer details
    print(f"Customer Details: {customer_details[['CustomerID', 'Name', 'Email']]}")

    # Get top 3 recommendations for the customer
    recommendations = top_n[customer_id]

    # Print recommendations
    print("\nTop 3 Recommendations:")
    for product_id, estimated_rating in recommendations:
        product_details = get_product_details(product_id)
        print(f"ProductID: {product_details['ProductID']}, PurchaseAmount: {product_details['PurchaseAmount']}, "
              f"Category1: {product_details['Category1']}, Category2: {product_details['Category2']}, "
              f"Estimated Rating: {estimated_rating}")

    # Choose a random marketing message
    chosen_message = marketing_messages.get(product_details['Category1'], 'Discover our new products!')

    # Print marketing message
    print(f"\nMarketing Message: {chosen_message}")

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

    print("\nEmail Draft:\n")
    print(email_draft)


# ... (previous code)

# ... (previous code)

# ... (previous code)

# Function to calculate evaluation metrics and print standard values
def evaluate_model(model, testset):
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)
    print(f"\nEvaluation Metrics:")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")

    # Interpretation of metrics
    print("\nInterpretation:")
    print("RMSE and MAE are standard metrics for evaluating prediction accuracy.")
    print("Lower values indicate better accuracy. Comparing with the scale of PurchaseAmount can provide context.")
    print("Here is a rough guide:")
    print("   - RMSE < 10% of the PurchaseAmount range: Good")
    print("   - RMSE ~ 20% of the PurchaseAmount range: Acceptable")
    print("   - RMSE > 30% of the PurchaseAmount range: Needs improvement")
    print(f"\n   - MAE < 10% of the PurchaseAmount range: Good")
    print(f"   - MAE ~ 20% of the PurchaseAmount range: Acceptable")
    print(f"   - MAE > 30% of the PurchaseAmount range: Needs improvement")

# Evaluate the model and print standard values
evaluate_model(model, testset)
