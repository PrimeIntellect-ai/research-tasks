You are an automation specialist managing a data ingestion workflow. Due to a bug in an upstream ETL job's retry mechanism, a recent batch of multi-lingual customer reviews was duplicated. To make matters worse, the retries went through different encoding pipelines, resulting in records that are logically identical but differ in Unicode normalization, casing, and trailing whitespace.

Your task is to write and execute a Python script (`/home/user/clean_reviews.py`) that reads the corrupted data, deduplicates it based on normalized text, and generates a clean dataset along with a processing report.

**Input Data:**
A JSONL (JSON Lines) file is located at `/home/user/reviews_raw.jsonl`. Each line is a JSON object with the following keys:
- `id` (string): Unique identifier for the record.
- `user` (string): User ID who submitted the review.
- `timestamp` (string): ISO 8601 timestamp (e.g., "2023-10-01T10:00:00Z").
- `text` (string): The text of the review.

**Processing Rules:**
1. **Normalization**: To determine if two records are duplicates, you must normalize the `text` field. Two records are considered duplicates if they have the same `user` and their `text` fields match *after* applying the following normalization steps:
   - Convert the text to Unicode NFC (Normalization Form C).
   - Strip all leading and trailing whitespace.
   - Convert the text to lowercase.
2. **Deduplication**: When duplicates are found (based on the composite key of `user` and `normalized_text`), keep only the record with the *earliest* `timestamp`. If the timestamps are identical, keep the record with the lexicographically *smallest* `id`.
3. **Sorting**: The final cleaned records must be sorted by `timestamp` in ascending order. If timestamps match, sort by `id` in ascending order.

**Output Requirements:**
1. **Clean Data**: Write the deduplicated, sorted records to `/home/user/reviews_clean.jsonl`. The output must be valid JSONL. Crucially, the records written to this file must retain their *original, unmodified* `text` values from the raw file (do not output the normalized version).
2. **Report**: Generate a text file at `/home/user/report.txt` exactly matching this template format:
   ```
   ETL Cleanup Report
   Total Input Records: {total_in}
   Total Valid Records: {total_out}
   Duplicates Removed: {duplicates}
   ```
   (Replace `{total_in}`, `{total_out}`, and `{duplicates}` with the actual integer counts).

You may use any standard library modules. Run your script to produce the output files before completing the task.