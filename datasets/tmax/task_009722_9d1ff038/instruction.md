You are a data analyst dealing with a messy dataset of app reviews. The data engineering team exported a CSV file, but the export tool had a bug that corrupted some unicode escape sequences in a JSON-encoded column, causing standard JSON parsers to crash.

Your task is to write a Python script that cleans the data, enforces quality constraints, extracts features, and calculates summary statistics. 

**Input File:**
`/home/user/data/raw_reviews.csv`

The CSV contains the following columns:
`review_id`, `timestamp`, `rating`, `review_text`, `metadata`

**Requirements:**

1. **Constraint-Based Data Validation:**
   - Drop any rows where `review_id` is not exactly 10 alphanumeric characters.
   - Drop any rows where `rating` is not an integer between 1 and 5 (inclusive).

2. **Data Cleaning & JSON Parsing (The Bug Fix):**
   - The `metadata` column contains JSON strings. However, some rows have malformed unicode escape sequences (e.g., `\u00X1`).
   - Find any literal `\u` followed by exactly 4 characters. If any of those 4 characters are NOT valid hexadecimal digits (0-9, a-f, A-F), replace that entire 6-character sequence with the literal string `[REDACTED]`.
   - After cleaning the string, parse it as JSON.
   - Extract the `device` field from the JSON. If the JSON parsing still fails, or if the `device` key is missing, assign the device as `"unknown"`.

3. **Feature Extraction:**
   - Calculate the `text_length` as the exact number of characters in the `review_text` column.

4. **Summary Statistics and Aggregation:**
   - Group the valid, cleaned dataset by the extracted `device` type.
   - For each device type, calculate:
     - `count`: Total number of valid reviews.
     - `avg_rating`: Average rating (rounded to 2 decimal places).
     - `avg_text_length`: Average `text_length` (rounded to 2 decimal places).

**Output:**
Save the aggregated results to `/home/user/output/summary.json`. 
The format must be a JSON dictionary where keys are the device types and values are dictionaries of the calculated statistics. 

Example Output Format:
```json
{
  "ios": {
    "count": 120,
    "avg_rating": 4.52,
    "avg_text_length": 45.12
  },
  "android": {
    "count": 95,
    "avg_rating": 3.90,
    "avg_text_length": 50.00
  }
}
```

Ensure your Python script runs correctly and creates the expected output file. You have terminal access to create scripts, directories, and run your code.