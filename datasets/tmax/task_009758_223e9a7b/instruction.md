You are an automation specialist for a product company. You need to build a robust data pipeline that ingests daily user feedback from multiple sources, cleans the messy text, deduplicates it using hashing, and schedules the job.

Your task is to write a Python script at `/home/user/process_feedback.py` that does the following:

1. **Read Inputs**: Read all files in the directory `/home/user/data/input/`. There are two file formats: CSV (`.csv`) and JSON (`.json`). 
   - CSV files have columns: `id`, `timestamp`, `comments`. Note that some comments contain embedded newlines which can break naive parsers.
   - JSON files contain a list of objects with the same keys: `id`, `timestamp`, `comments`.

2. **Normalize Text**: For each record, normalize the `comments` field:
   - Replace any sequence of whitespace characters (spaces, tabs, newlines, etc.) with a single space.
   - Strip leading and trailing whitespace.
   - Convert the entire string to lowercase.

3. **Hash & Deduplicate**: 
   - Calculate the SHA-256 hexadecimal digest of the *normalized* comment.
   - We receive duplicate feedback across different channels. Deduplicate the records based on this SHA-256 hash.
   - If multiple records have the same hash, keep ONLY the record with the earliest `timestamp` (using standard lexicographical string comparison is fine as timestamps are in ISO 8601 format).

4. **Output**: 
   - Write the deduplicated records to a JSON Lines file at `/home/user/data/output/clean_feedback.jsonl`.
   - Each line must be a valid JSON object containing exactly these keys: `hash` (the SHA-256 hex digest), `id`, `timestamp`, and `normalized_comment`.
   - The records in the output file can be in any order.

5. **Schedule**: 
   - Run your script once so the output file is generated.
   - Then, set up a user cron job that schedules `/usr/bin/python3 /home/user/process_feedback.py` to run every day exactly at 02:00 AM server time.

Ensure the output directory exists before writing to it.