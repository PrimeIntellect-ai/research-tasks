You are a data scientist tasked with cleaning a messy dataset of multilingual product reviews. The previous pipeline was built using basic shell tools and silently dropped records because the `review_text` field contains embedded newlines inside quoted CSV fields. 

Your goal is to write a robust Python script to process this data, clean it, and extract aggregate statistics.

**Input Data:**
A CSV file located at `/home/user/raw_reviews.csv` with the following columns:
1. `timestamp` (ISO 8601 format, e.g., `2023-01-15T10:00:00Z`)
2. `user_id` (String)
3. `review_text` (String, contains multilingual text, varying Unicode normalization forms, and embedded newlines)
4. `rating` (Integer from 1 to 5, occasionally missing or malformed)

**Requirements:**
Write and execute a Python script that reads the input CSV and performs the following data cleaning and aggregation pipeline:

1. **Filtering & Cleaning**:
   - Drop any row where the `rating` is empty, not a number, or missing.
   - Replace any embedded newlines (`\n` or `\r\n`) within the `review_text` field with a single space character (` `).
   - Normalize the `review_text` using **Unicode NFKC** normalization.

2. **Deduplication**:
   - A user may have submitted multiple reviews. Keep only the **most recent** review for each `user_id` based on the `timestamp` column.

3. **Output Cleaned Data**:
   - Save the cleaned, deduplicated records to `/home/user/cleaned_reviews.jsonl` as a JSON Lines file.
   - Each line must be a valid JSON object with keys: `"timestamp"`, `"user_id"`, `"review_text"`, and `"rating"` (rating must be an integer).

4. **Time-based Aggregation**:
   - Bucket the cleaned data by month (using the format `YYYY-MM`).
   - For each month, calculate:
     - `total_reviews`: Count of valid reviews.
     - `avg_rating`: Average rating (rounded to 2 decimal places).
     - `avg_review_length`: Average length of the normalized `review_text` in characters (rounded to 2 decimal places).
   - Save these aggregations to `/home/user/monthly_stats.csv`.
   - The CSV must have headers `month,total_reviews,avg_rating,avg_review_length` and be sorted chronologically by month.

You may install any standard Python packages (like `pandas`) using `pip` if needed, though the Python standard library is sufficient.