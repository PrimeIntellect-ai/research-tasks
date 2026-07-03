You are a localization engineer managing translation usage telemetry for a global app. Your system receives time-series usage data from different regional servers in different formats. You need to write a Go program to clean, normalize, deduplicate, and merge these logs into a standardized time-series dataset.

The raw telemetry data is located in `/home/user/loc_data/`:
1. `/home/user/loc_data/eu_logs.csv`: A CSV file containing European telemetry.
   - Columns: `timestamp` (String in `DD/MM/YYYY HH:MM:SS` format, assumed UTC), `lang_code` (e.g., `FR-fr`), `translation_key`, `usage_count` (integer).
2. `/home/user/loc_data/asia_logs.json`: A JSON array containing Asian telemetry.
   - Fields: `time_logged` (Unix epoch timestamp integer in seconds), `locale` (e.g., `ja_JP`), `key`, `uses` (integer).

Write a Go program (save it anywhere, e.g., `/home/user/process.go`) and run it to produce a final dataset at `/home/user/normalized_timeseries.jsonl` with the following requirements:

1. **Format:** Output must be a JSON Lines (.jsonl) file.
2. **Standardized Schema:** Each line must be a JSON object containing exactly these fields:
   - `timestamp`: A string formatted strictly as RFC3339 in UTC (e.g., `"2023-04-15T14:30:00Z"`).
   - `locale`: A normalized string representing the language/locale. It must be strictly lowercase, using a hyphen `-` as the separator instead of an underscore (e.g., `FR-fr`, `fr_FR`, and `fr-FR` must all become `fr-fr`).
   - `key`: The translation key string (unchanged).
   - `usage_count`: The integer count of uses.
3. **Deduplication:** If multiple records in the combined data have the exact same normalized `timestamp`, `locale`, and `key`, you must deduplicate them by keeping only the record with the **maximum** `usage_count` (do not sum them).
4. **Sorting:** The final JSONL output must be strictly sorted chronologically by the normalized `timestamp` (oldest to newest). If timestamps are identical, sort alphabetically by `locale`, then by `key`.

Please execute your Go program so that `/home/user/normalized_timeseries.jsonl` is generated with the correct data.