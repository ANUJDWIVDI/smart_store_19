import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from collections import defaultdict

# Load the data from the Excel file
file_path = 'sample_data.xlsx'
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

# Print the top 3 recommended products for each user
for uid, user_ratings in top_n.items():
    print(f"Top 3 recommendations for Customer {uid}: {user_ratings}")
