You are a data engineer tasked with building an ETL pipeline that cleans a product dataset, extracts features, and generates product recommendations using similarity search.

The raw dataset is located at `/home/user/raw_data.csv`. It contains the following columns: `item_id`, `category`, `price`, and `rating`.

Perform the following steps:
1. **Dependency Installation**: Install `pandas` and `scikit-learn` if they are not already installed.
2. **Data Cleaning & Outlier Handling**:
   - Read `/home/user/raw_data.csv`.
   - Remove any rows where `price` is less than 0 or greater than 1000 (these are outliers).
3. **Missing Value Handling**:
   - Impute missing `price` values with the overall median of the valid `price` values from the remaining dataset.
   - Impute missing `rating` values with `0.0`.
4. **Feature Engineering**:
   - Normalize the cleaned `price` and `rating` columns using Min-Max scaling (so their values range exactly between 0 and 1).
   - One-hot encode the `category` column (ensure the resulting columns are sorted alphabetically by category name).
5. **Similarity Search**:
   - Construct a feature vector for each item consisting of the scaled `price`, scaled `rating`, and the one-hot encoded categories.
   - Compute the pairwise Cosine Similarity between all remaining items.
   - For each item, find the top 2 most similar items (excluding itself). If there is a tie in similarity score, prioritize the item with the smaller `item_id`.
6. **Output**:
   - Save the recommendations to `/home/user/recommendations.json`.
   - The JSON should be a dictionary where the keys are the `item_id`s (as strings) and the values are lists of the 2 recommended `item_id`s (as integers). 
   - Example format: `{"101": [105, 109], "103": [104, 108]}`

Ensure your pipeline processes the data exactly according to these rules and writes the final JSON file.