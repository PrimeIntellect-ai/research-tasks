You are a log analyst investigating application performance patterns. You have been given a raw CSV log file at `/home/user/raw_logs.csv` containing trace data. However, previous attempts to process this file failed or produced inaccurate results because many log entries contain embedded newlines in their `message` field (e.g., multi-line stack traces). 

You need to build a robust data processing pipeline using Python and a `Makefile` to orchestrate the workflow.

**Objective:**
Build a 3-stage pipeline orchestrated by a `Makefile` that correctly parses the data, groups/sorts it, and calculates rolling statistics.

**Pipeline Stages:**

1. **Extraction (`step1_parse.py`):**
   - Read `/home/user/raw_logs.csv`. The file has columns: `timestamp`, `session_id`, `response_time`, and `message`.
   - Correctly parse the CSV, handling the embedded newlines in the quoted `message` field. Do not drop these multi-line rows.
   - Filter out any rows where `session_id` is empty or missing.
   - Output the valid records to `/home/user/parsed_logs.json` as a JSON array of objects.

2. **Sorting & Grouping (`step2_sort_group.py`):**
   - Read `/home/user/parsed_logs.json`.
   - Group the records by `session_id`.
   - Within each group, sort the records strictly by `timestamp` in ascending order.
   - Output the result to `/home/user/grouped_logs.json`. The format should be a JSON object mapping each `session_id` (string) to an array of its sorted records.

3. **Rolling Statistics (`step3_stats.py`):**
   - Read `/home/user/grouped_logs.json`.
   - For each `session_id`, calculate the rolling average of the `response_time` using a window size of 3 records. (If a window has fewer than 3 records, e.g., the first or second record, average the available records).
   - Find the *maximum* rolling average achieved during each session.
   - Output to `/home/user/rolling_stats.json` as a JSON object mapping `session_id` to its maximum rolling average, rounded to exactly 2 decimal places.

**Orchestration:**
Create a `Makefile` in `/home/user` with the following targets:
- `parse`: Runs `step1_parse.py`. Depends on `raw_logs.csv` and `step1_parse.py`.
- `group`: Runs `step2_sort_group.py`. Depends on `parsed_logs.json` and `step2_sort_group.py`.
- `stats`: Runs `step3_stats.py`. Depends on `grouped_logs.json` and `step3_stats.py`.
- `all`: The default target that ensures `rolling_stats.json` is built.
- `clean`: Removes all generated JSON files.

Once you have written the scripts and the `Makefile`, run `make all` to generate the final `/home/user/rolling_stats.json`.