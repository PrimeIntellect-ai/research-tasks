You are a data analyst tasked with matching product catalogs from two different suppliers and training a simple pricing/rating model. 

You have two CSV files located at:
- `/home/user/supplier_a.csv`
- `/home/user/supplier_b.csv`

Both files have the following columns: `id`, `desc`, `price`, `rating`.
Some rows have missing values for `price` or `rating` (represented as empty strings).

Write a Python script (e.g., `/home/user/solution.py`) to perform the following steps:

1. **Missing Value Handling**: For both datasets independently, fill missing `price` values with the median price of that dataset. Fill missing `rating` values with the mean rating of that dataset.

2. **Embedding & Retrieval (Data Joining)**:
   - Compute TF-IDF embeddings for the `desc` column of both datasets combined (fit a single `TfidfVectorizer` from `sklearn.feature_extraction.text` on all descriptions from both A and B, using default parameters).
   - For every product in Supplier A, find the single most similar product in Supplier B using Cosine Similarity on these TF-IDF vectors.
   - If there is a tie in similarity, pick the product from B with the lexicographically smaller `id`.

3. **Regression**:
   - Create a joined dataset where each row represents a product from A and its matched product from B.
   - Train a standard Linear Regression model (`sklearn.linear_model.LinearRegression` with default parameters) on this joined dataset.
   - **Features (X)**: `price` from A, `price` from B, `rating` from B.
   - **Target (y)**: `rating` from A.
   - Predict the `rating` for A using this trained model on the same training data.

4. **Output generation**:
   Create a CSV file at `/home/user/predictions.csv` with exactly the following columns, in this order:
   `id_A,matched_id_B,similarity_score,predicted_rating_A`
   
   Format requirements for the output CSV:
   - Include a header row.
   - Round `similarity_score` and `predicted_rating_A` to exactly 4 decimal places.
   - Sort the output rows alphabetically by `id_A`.

Note: You do not need to split the data into train/test sets. Train and predict on the entire joined dataset. You can assume `scikit-learn`, `pandas`, and `numpy` are installed in the environment.