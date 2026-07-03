You are helping a researcher organize their dataset processing pipeline. They have written a Python script to prepare item features for a recommendation system, but they suspect there is a critical "data leakage" issue causing their downstream validation metrics to be artificially inflated.

The script is located at `/home/user/build_recs.py` and processes the dataset `/home/user/item_features.csv`.

Currently, the script applies standardization and Principal Component Analysis (PCA) to the *entire* dataset before splitting it into training and testing sets. 

Your tasks are to:
1. **Fix the Data Leakage**: Rewrite the script to use a `sklearn.pipeline.Pipeline`. The pipeline should contain a `StandardScaler` and a `PCA` (with `n_components=5`, `random_state=42`).
2. **Correct Splitting**: Split the raw data into training and testing sets *first* (`test_size=0.2`, `random_state=42`, `shuffle=True`). 
3. **Fit and Transform**: Fit the pipeline strictly on the training set, then transform both the training and testing sets.
4. **Covariance/Correlation Analysis**: Calculate the Pearson correlation matrix of the 5 PCA features within the transformed *test* set. Compute the mean of the absolute values of the lower triangle of this correlation matrix (strictly below the main diagonal, excluding the diagonal itself). Save this single numeric value (rounded to 6 decimal places) to `/home/user/test_corr_mean.txt`.
5. **Similarity Search**: The researcher wants to test the recommendation logic. Using cosine similarity on the newly transformed features, find the 3 most similar items in the *training* set to the *first item* (index 0) of the *test* set. Save the 0-based integer indices of these 3 training items (relative to the `X_train` array) to `/home/user/recommendations.txt` as a single comma-separated line (e.g., `45,120,3`).

Ensure all files are created in `/home/user/` and contain only the requested values.