You are a localization engineer managing the translation workflows for a global software release. You need to build a time-series data processing pipeline using **Bash** and standard UNIX utilities (`jq`, `awk`, etc.) to track translator productivity over time.

You have a raw stream of translation edit logs in JSONL format.
The file is located at `/home/user/raw_edits.jsonl`.
Each line looks like this:
`{"timestamp": "2023-10-01T08:15:00Z", "locale": "fr-FR", "words": 100, "tm_match": 80}`

Your task is to write a bash script `/home/user/process_loc.sh` that performs the following time-series processing:

1. **Feature Extraction:** For each event, calculate the `effective_words`. 
   The formula is: `effective_words = words * (tm_match / 100)`. (All inputs guarantee this results in a whole number).
2. **Resampling:** Group the events into 1-hour intervals based on the `timestamp` (e.g., `2023-10-01T08:15:00Z` and `2023-10-01T08:45:00Z` both fall into the `2023-10-01T08:00:00Z` bucket). Calculate the sum of `effective_words` for each locale in that hour.
3. **Gap-Filling:** The pipeline must report hourly metrics for exactly three locales: `de-DE`, `es-ES`, and `fr-FR`, and strictly cover the time range from `2023-10-01T08:00:00Z` to `2023-10-01T12:00:00Z` (inclusive of the 08:00, 09:00, 10:00, 11:00, and 12:00 buckets). If a locale has no edits during an hour, output `0` for `effective_words`.
4. **Output Format:** Write the final gap-filled, aggregated results to `/home/user/hourly_loc_stats.csv`. 
   The CSV must have a header: `timestamp,locale,effective_words`.
   The rows must be sorted chronologically by timestamp, and then alphabetically by locale.
5. **Pipeline Logging:** The script must log its execution to `/home/user/process.log`. 
   - Before processing starts, append: `[<CURRENT_DATETIME>] PIPELINE_START`
   - After writing the CSV, append: `[<CURRENT_DATETIME>] PIPELINE_END - Processed <N> events` (where `<N>` is the exact number of lines read from `raw_edits.jsonl`).

Run your script to produce the final CSV and log file.