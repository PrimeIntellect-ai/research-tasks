You are a localization engineer at a software company. Your team uses a Translation Memory (TM) to help translators. You want to analyze a recent log of translation activities to see how much the source texts provided to translators deviate from the source texts already in your TM, and how this deviation fluctuates over time.

You have been provided with two files in your home directory (`/home/user/`):
1. `tm.csv`: A CSV file containing your current translation memory. It has two columns: `source` and `target`.
2. `activity.json`: A JSON array of translation events. Each event is a dictionary with keys: `time`, `source`, and `input`. The `time` field contains a timestamp string that includes timezone offsets.

Your task is to write and execute a Python script that does the following:
1. **Timestamp Parsing and Alignment:** Parse the `time` field of each event in `activity.json`. Convert all timestamps to UTC.
2. **Time-Based Bucketing:** Group the events into 1-hour time buckets based on their UTC time. A bucket starts exactly at the top of the hour (e.g., `2023-10-01T12:00:00Z`).
3. **Similarity Computation:** For every event, compute the standard Levenshtein edit distance (where insertions, deletions, and substitutions each have a cost of 1) between the event's `source` text and **every** `source` text present in `tm.csv`. Find the *minimum* edit distance for that event (i.e., the distance to the closest matching string in the TM).
4. **Aggregation:** For each 1-hour bucket, calculate the *average* minimum edit distance across all events that fall into that bucket.
5. **Output:** Generate a CSV report located at `/home/user/bucket_analysis.csv` with exactly two columns: `bucket_utc` and `avg_min_distance`. 
    - `bucket_utc` must be formatted strictly as an ISO 8601 string ending in 'Z' (e.g., `2023-10-01T10:00:00Z`).
    - `avg_min_distance` must be rounded to exactly 2 decimal places (e.g., `3.50`).
    - The CSV must include a header row and be sorted chronologically by `bucket_utc`.
    - If a bucket has no events, it should not appear in the final CSV.

Please write the Python code, execute it, and ensure the `/home/user/bucket_analysis.csv` is created exactly as specified.