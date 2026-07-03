You are a data scientist tasked with cleaning a messy, multi-lingual dataset of product reviews. The dataset is currently in a malformed CSV format with various constraint violations, mixed Unicode normalization forms, and some invalid UTF-8 bytes.

You need to write a Rust command-line tool to perform a multi-stage ETL (Extract, Transform, Load) pipeline.

Here are the requirements:

1. **Project Setup**:
   Create a new Rust binary project named `dataset_cleaner` in `/home/user/dataset_cleaner`.
   You may use external crates like `csv`, `serde`, `serde_json`, and `unicode-normalization`.

2. **Input**:
   The input file is located at `/home/user/raw_reviews.csv`.
   It does NOT have a header row. 
   The columns are: `id`, `language`, `rating`, `text`.

3. **Data Validation & Cleaning Rules**:
   Process each row according to the following constraints. If a row violates ANY of the constraints for `id`, `language`, or `rating`, or if the `text` is empty after cleaning, **drop the row** entirely.
   
   *   `id`: Must be exactly 8 alphanumeric characters (a-z, A-Z, 0-9).
   *   `language`: Must be exactly 2 lowercase alphabetical characters (e.g., "en", "fr").
   *   `rating`: Must be an integer between 1 and 5 (inclusive).
   *   `text`: 
       *   First, decode the bytes. Any invalid UTF-8 sequences must be replaced with the Unicode replacement character (`U+FFFD`).
       *   Second, normalize the valid UTF-8 text to Unicode Normalization Form C (NFC).
       *   Third, trim any leading and trailing whitespaces.
       *   Finally, if the resulting string is empty, drop the row.

4. **Output**:
   Write the cleaned, valid records to `/home/user/clean_reviews.jsonl`.
   The output must be in JSON Lines format (one JSON object per line).
   The JSON objects must have the following keys:
   *   `id` (string)
   *   `lang` (string)
   *   `score` (integer, from the rating column)
   *   `content` (string, the cleaned text)

5. **Execution**:
   Compile your Rust program in release mode (`cargo build --release`) and run it to process the dataset.

Your final deliverable is the successfully generated `/home/user/clean_reviews.jsonl` file.