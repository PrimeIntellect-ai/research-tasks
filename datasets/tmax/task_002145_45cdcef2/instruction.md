You are an AI assistant helping a researcher organize and preprocess a messy text dataset for a downstream machine learning experiment. 

You have been provided with a dataset at `/home/user/raw_dataset.csv`. It contains the following columns: `id`, `text`, `author_age`.

Your task is to write and execute a Python script that performs the following steps:

1. **Missing Value & Outlier Handling:**
   - Load the CSV file.
   - Drop any rows where the `text` column is missing (NaN) or is an empty string.
   - For the `author_age` column, valid ages are defined as strictly between 15 and 100 (inclusive). Any ages outside this range, or missing (NaN), are considered outliers/missing. Calculate the median of the **valid** ages. Replace all invalid or missing ages with this median value.

2. **Tokenization and Dataset Preparation:**
   - Process the cleaned `text` column using TF-IDF. Use `sklearn.feature_extraction.text.TfidfVectorizer` with `max_features=50`, `lowercase=True`, and default tokenization (which is suitable for this text). Fit and transform the text into a feature matrix.

3. **Dimensionality Reduction:**
   - Apply Principal Component Analysis (PCA) to the dense representation of the TF-IDF matrix to reduce it to exactly 2 dimensions. Use `sklearn.decomposition.PCA` with `n_components=2` and `random_state=42`.

4. **Large-Scale Data Storage:**
   - Save the processed data into a Parquet file at `/home/user/processed_data.parquet`. The Parquet file must contain exactly three columns in this order: `id` (from the cleaned dataframe), `pca_1` (the first principal component), and `pca_2` (the second principal component).

5. **Experiment Tracking:**
   - Create a JSON file at `/home/user/experiment_log.json` tracking the experiment metrics. It must contain exactly the following keys and accurate values:
     - `"initial_rows"`: (integer) The number of rows in the original raw dataset.
     - `"cleaned_rows"`: (integer) The number of rows after dropping missing/empty text.
     - `"median_age_used"`: (float) The median age that was used to impute invalid ages.
     - `"explained_variance_ratio_sum"`: (float) The sum of the `explained_variance_ratio_` of the two PCA components, rounded to exactly 4 decimal places.

Ensure your Python code is executed and both `/home/user/processed_data.parquet` and `/home/user/experiment_log.json` are generated successfully.