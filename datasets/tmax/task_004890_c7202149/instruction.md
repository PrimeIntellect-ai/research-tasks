You are an ETL data engineer working on a daily feedback pipeline. The raw data arrives in a "wide" format where each column is a specific date, but our analytics team needs it processed into a normalized, gap-filled, and hash-deduplicated structure.

You have been provided with a raw CSV file at `/home/user/raw_feedback.csv`.

Perform the following steps using Python:

1. **Wide-to-Long Reshaping:** Convert the dataset from wide format to long format. The resulting columns should be `user_id`, `date`, and `feedback`.
2. **Resampling & Gap-Filling:** The dates in the columns currently span from `2023-11-01` to `2023-11-04`, but `2023-11-02` is completely missing from the input columns. You must inject rows for `2023-11-02` (and any other missing days between the min and max date) for every `user_id`. The `feedback` for these gap-filled dates should be an empty string `""`. Treat any missing (`NaN` or null) feedback in existing days as empty strings `""` as well.
3. **Tokenization & Normalization:** For all non-empty feedback strings:
    * Convert the text to lowercase.
    * Remove all punctuation (keep only alphanumeric characters `a-z`, `0-9`, and spaces).
    * Replace multiple consecutive spaces with a single space.
    * Strip leading and trailing whitespace.
4. **Hash-based Deduplication:** 
    * Compute the MD5 hash of the normalized feedback text (encoded as UTF-8).
    * For empty strings `""`, the hash should also be an empty string `""` (do NOT compute the MD5 of an empty string).
5. **Output Generation:**
    * Save the processed long-format dataset to `/home/user/processed_logs.csv` with columns: `user_id,date,text_hash`. Sort this CSV first by `user_id` (ascending) and then by `date` (ascending).
    * Save a deduplicated dictionary to `/home/user/hash_mapping.json` mapping the MD5 hash (key) to its corresponding normalized text (value) so the analytics team can lookup the text. Do not include the empty string in this mapping.

Write and execute a Python script to perform this exact workflow. Ensure the final files exist at the exact paths specified.