You are an automation specialist building a log analysis workflow. Your task is to write a Python script that extracts unstructured log messages, normalizes them, maps them to known error categories using text similarity, and logs the pipeline's execution.

**Input Files:**
1. `/home/user/logs.txt` - A raw text file containing application logs.
   Format: `YYYY-MM-DD HH:MM:SS | LEVEL | MESSAGE`
2. `/home/user/categories.csv` - A CSV file containing known error categories and reference keywords.
   Format: `category_name,reference_text`

**Requirements:**
Write a Python script at `/home/user/process_logs.py` that performs the following steps:

1. **Information Extraction**: Parse `/home/user/logs.txt` to extract the `timestamp`, `level`, and `message` from each line.
2. **Tokenization and Normalization**:
   - For both the log `message` and the `reference_text` from the CSV:
     - Convert the text to lowercase.
     - Replace any character that is not a letter (a-z) or a number (0-9) with a single space.
     - Split the resulting string by whitespace into a set of unique words (tokens).
3. **Similarity Computation**:
   - For each log message, compute the Jaccard similarity score against all `reference_text` token sets from the CSV.
   - Jaccard similarity is defined as the size of the intersection divided by the size of the union of the two token sets.
   - Assign the log to the `category_name` with the highest similarity score.
   - If the maximum similarity score across all categories is exactly `0.0`, assign the category as `"Unknown"`.
   - If there is a tie for the highest score, pick the category that appears first in the CSV.
4. **Output Generation**:
   - Write the processed logs to a JSON Lines file at `/home/user/mapped_errors.jsonl`.
   - Each line should be a JSON object with the exact keys: `{"timestamp": "...", "level": "...", "category": "..."}`.
5. **Pipeline Logging**:
   - Append a single log line to `/home/user/pipeline.log` exactly matching this format:
     `[INFO] Processed <N> logs, <M> matched, <K> unknown`
     *(Where N is the total logs read, M is the number assigned to a known category, and K is the number assigned to "Unknown".)*

Run your script to produce the final `mapped_errors.jsonl` and `pipeline.log` files.