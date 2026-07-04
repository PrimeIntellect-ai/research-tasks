You are a data analyst tasked with cleaning and extracting insights from a messy, multi-lingual customer feedback dataset. 

You have been provided with a raw data file at `/home/user/raw_feedback.csv`.

Write a Python script named `/home/user/process_feedback.py` to process this file and generate a summary report. You may install any standard Python packages (like `pandas` or `regex`) using `pip`.

**Data Processing Rules:**
Read `/home/user/raw_feedback.csv`, which has the following columns: `id`, `timestamp`, `user_metadata`, and `feedback_text`.
You must filter the dataset and process the valid rows according to these strict rules:

1. **Timestamp Validation:** Discard any row where the `timestamp` does not exactly match the format `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2023-10-15T14:30:00Z`).
2. **IP Extraction & Validation:** The `user_metadata` column contains messy text. You must extract an IPv4 address from it using regex. To be valid, the IPv4 address must consist of four dot-separated integers between 0 and 255. Discard the row if no valid IPv4 address is found.
3. **Region Extraction:** The `user_metadata` column also contains a region identifier in the format `Region: <Code>` (e.g., `Region: NA`, `Region: EU`). Extract this 2-letter code. If missing, default to `UNKNOWN`.
4. **Rating Extraction:** The `feedback_text` contains an embedded rating in the format `[RATING: X]` or `[RATING:X]`, where `X` is an integer from 1 to 5. Extract this integer. Discard the row if the rating is missing or not between 1 and 5.
5. **Unicode Processing:** For the valid rows, analyze the `feedback_text`. Count the total number of non-ASCII alphanumeric characters across all valid rows. A character is considered a non-ASCII alphanumeric if it is alphanumeric (e.g., `.isalnum()` in Python is True) AND its Unicode code point is strictly greater than 127.

**Aggregation & Output:**
After processing the rows, calculate summary statistics and write them to `/home/user/summary.json` with the exact following structure:
```json
{
  "total_valid_rows": <int>,
  "average_rating": <float, rounded to 2 decimal places>,
  "region_counts": {
    "<Region_1>": <int>,
    "<Region_2>": <int>
  },
  "total_non_ascii_alnum": <int>
}
```

Run your script to ensure `/home/user/summary.json` is generated correctly.