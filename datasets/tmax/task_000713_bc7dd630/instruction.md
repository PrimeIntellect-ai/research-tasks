You are a data engineer building an ETL pipeline to process activity logs from multiple applications. 

You have been provided an incomplete, wide-format CSV log file at `/home/user/activity_wide.csv`. The file records activity states for three applications (`AppAlpha`, `AppBeta`, `AppGamma`) at 15-minute intervals. 

However, there are several issues with the data:
1. **Missing Intervals:** Some 15-minute timestamps are completely missing from the file.
2. **Wide Format:** The data is column-oriented by application, making it hard to query.
3. **Messy Text:** The activity text contains inconsistent capitalization and punctuation.

Write a Go program (e.g., `/home/user/process.go`) that performs the following ETL tasks:

**1. Resampling and Gap-Filling**
The data should cover the time range from `2023-10-01T10:00:00Z` to `2023-10-01T11:45:00Z` inclusive, at strictly 15-minute intervals (e.g., 10:00, 10:15, 10:30, etc. - exactly 8 intervals). 
Detect any missing 15-minute intervals in the sequence and insert them. For any newly inserted rows, or if a cell in an existing row is completely empty, the raw activity state for that app should be considered the exact string `NONE`.

**2. Wide-Long Reshaping**
Convert the data from wide format (`Timestamp, AppAlpha, AppBeta, AppGamma`) into a logical long format: `Timestamp, AppName, RawActivity`.

**3. Tokenization and Normalization**
For each raw activity string:
- Convert all characters to lowercase.
- Replace any non-alphanumeric character (e.g., `-`, `_`, `:`) with a single space.
- Collapse any multiple consecutive spaces into a single space, and trim leading/trailing spaces.
- If the normalized string is empty or was originally the `NONE` state (which normalizes to `none`), use the exact string `no_action`.

**4. Summary Statistics / Aggregation**
For each application, count the total occurrences of each normalized activity token across the entire time window.

**5. Output**
Write the aggregated counts to `/home/user/token_counts.json` in the following exact JSON format (indented by 2 spaces):
```json
{
  "AppAlpha": {
    "login success": 2,
    "no_action": 6
  },
  "AppBeta": { ... },
  "AppGamma": { ... }
}
```

Run your Go program so the output file is generated correctly.