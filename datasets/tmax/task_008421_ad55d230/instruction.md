You are tasked with building a data processing pipeline to analyze a dataset of multi-language social media posts. The raw data is located at `/home/user/raw_posts.csv`.

You need to write a Python script that processes this CSV file and outputs a JSON file at `/home/user/aggregated_results.json` containing time-bucketed aggregations.

Here are the precise requirements for your processing pipeline:

1. **Environment Setup:** You may use standard Python libraries, or install packages like `pandas` or `pytz` as needed. Run your code in the provided `/home/user` directory.
2. **Time-Based Bucketing:**
   - Parse the `timestamp` column (provided in ISO 8601 format, UTC).
   - Group the records into fixed **4-hour intervals** starting at midnight UTC (e.g., `00:00:00` to `03:59:59`, `04:00:00` to `07:59:59`, etc.).
   - The bucket identifier should be the start time of the interval formatted as a strict ISO 8601 UTC string (e.g., `"2023-11-15T04:00:00Z"`).
3. **Unicode and Text Processing:**
   - Extract the `content` column for each row.
   - First, apply **NFKC** (Normalization Form Compatibility Composition) Unicode normalization to the text.
   - Second, split the normalized text into "words" using standard whitespace splitting (i.e., Python's default `str.split()`).
   - Identify the longest word in each 4-hour bucket by character count (after normalization).
   - *Tie-breaker rules:* If multiple words in a bucket have the same maximum character length, select the one that appeared earliest in the chronological sorting of the timestamps. If they appear in the same post, select the one that appears first in the text.
4. **Output Format:**
   - Save the results to `/home/user/aggregated_results.json`.
   - The JSON should be an object where the keys are the 4-hour bucket identifiers (only include buckets that have at least one record).
   - The value for each key must be an object containing:
     - `"record_count"`: The integer number of posts in this time bucket.
     - `"longest_word"`: The longest NFKC-normalized word found in this bucket.

Example Output format:
```json
{
  "2023-11-15T00:00:00Z": {
    "record_count": 15,
    "longest_word": "antidisestablishmentarianism"
  },
  "2023-11-15T08:00:00Z": {
    "record_count": 3,
    "longest_word": "こんにちは"
  }
}
```

Ensure your pipeline runs successfully and produces the exact specified JSON schema.