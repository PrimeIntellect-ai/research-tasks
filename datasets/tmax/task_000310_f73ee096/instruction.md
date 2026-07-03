You are acting as a localization engineer. Our translation ingestion ETL job has a bug: when it retries failed batches, it appends duplicate translation records instead of updating them. Furthermore, we need to anonymize translator data before sharing the files with the analytics team, and compute some rolling statistics.

Your task is to create an idempotent Bash processing pipeline to clean this data and schedule it.

**Input Data:**
There is a CSV file at `/home/user/incoming/loc_drops.csv`.
The CSV has no header. The columns are:
1. `translation_id` (string)
2. `language_code` (string, e.g., fr, es, de)
3. `timestamp` (integer, Unix epoch)
4. `translator_email` (string)
5. `word_count` (integer)

**Requirements:**

1. **Script Creation:** Create a bash script at `/home/user/process_loc.sh`. Make sure it is executable.
2. **Deduplication:** The script must read `/home/user/incoming/loc_drops.csv`. If multiple rows have the same `translation_id` and `language_code`, keep ONLY the row with the highest `timestamp`.
3. **Data Masking:** Anonymize the `translator_email` in the deduplicated data by replacing the entire domain (everything after the `@`) with `anonymized.local`. For example, `alice@example.com` becomes `alice@anonymized.local`.
4. **Cleaned Output:** Save the deduplicated, anonymized records to `/home/user/output/cleaned.csv`. The output must be comma-separated and sorted numerically by `timestamp` in ascending order.
5. **Cumulative Statistics:** Calculate the cumulative total of `word_count` over time for each `language_code`.
   Output this to `/home/user/output/cumulative_stats.csv`.
   Format: `timestamp,language_code,cumulative_word_count`
   This file must also be sorted numerically by `timestamp` ascending. If multiple unique records have the exact same timestamp, their word counts should be added to the cumulative total for that language *before* outputting the row for that timestamp (output one row per timestamp per language).
6. **Pipeline Scheduling:** Set up a user cron job to run `/home/user/process_loc.sh` every day at exactly 03:15 AM.

Create the `/home/user/output` directory if it does not exist. The script should run successfully with standard Linux tools (`awk`, `sort`, `sed`, etc.).