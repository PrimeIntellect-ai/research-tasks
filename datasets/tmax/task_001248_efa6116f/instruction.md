You are tasked with cleaning a dataset of product reviews, engineering text-based features, and computing a correlation matrix. The dataset contains hidden type issues caused by silent float conversions from missing values and dirty data.

**Data Source:**
A CSV file located at `/home/user/raw_data.csv` containing the following columns:
- `review_id`: A unique identifier (has some corrupted float values like `103.0` instead of `103`).
- `user_score`: Integer rating from 1 to 5.
- `upvotes`: Number of upvotes. Contains missing values (which caused pandas to silently cast the column to float).
- `review_text`: The text of the review.

**Your Objectives:**

1. **Data Cleaning:**
   - Load the CSV file using Python (pandas is recommended).
   - Fill any missing values in the `upvotes` column with `0`.
   - Convert both `review_id` and `upvotes` to strict integers. (e.g. `103.0` must become `103`).

2. **Tokenization & Feature Engineering:**
   - Process the `review_text` column to create two new numeric features: `token_count` and `avg_token_length`.
   - **Tokenization rules:** First, convert the text to lowercase. Then, remove all characters that are NOT alphanumeric or whitespace (i.e., remove punctuation). Finally, split the text by whitespace into a list of tokens.
   - `token_count`: The number of tokens in the processed text.
   - `avg_token_length`: The average length of the tokens in the processed text. (If `token_count` is 0, set `avg_token_length` to 0.0).

3. **Correlation Analysis:**
   - Compute the Pearson correlation matrix for the following four columns: `user_score`, `upvotes`, `token_count`, and `avg_token_length`.
   - Round the correlation values to 4 decimal places.

4. **Outputs:**
   - Save the cleaned and enriched dataset to `/home/user/cleaned_data.csv`. The output must be comma-separated, include the header, and not contain the dataframe index. It must contain exactly these columns in order: `review_id`, `user_score`, `upvotes`, `review_text`, `token_count`, `avg_token_length`.
   - Save the correlation matrix as a JSON file at `/home/user/correlation.json`. It should be a nested dictionary representing the matrix (e.g., `{"user_score": {"user_score": 1.0000, "upvotes": 0.5342, ...}, ...}`).

Ensure your script handles everything programmatically and generates the exact filenames requested.