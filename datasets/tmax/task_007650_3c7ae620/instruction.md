You are acting as a localization engineer. Our team tracks localization engagement (views) and translation string updates (edits) across our software platforms. The data comes from two different legacy systems and is heavily fragmented. 

Your task is to write a Go program that processes this data into a unified, clean, daily report.

You have two input files located in `/home/user/workspace`:
1. `loc_views.csv`: A log of user views of localized strings. It is in "long" format but has irregular timestamps.
   Columns: `timestamp,lang,views` (e.g., `2023-10-01T10:00:00Z,fr,150`)
2. `loc_edits.json`: A log of translation edits by language. It is in "wide" format and contains missing values.
   Format: Array of objects like `{"time": "2023-10-01T12:00:00Z", "fr": 5, "de": null}`

You need to write a Go program (`/home/user/workspace/process_loc.go`) that performs the following:
1. **Pipeline DAG Orchestration**: The program must implement a concurrent data pipeline using Go channels. It should have independent goroutines for reading the CSV, reading the JSON, processing/merging the data, and writing the output.
2. **Timestamp Alignment**: Parse all timestamps (RFC3339) and truncate them to the day (`YYYY-MM-DD`).
3. **Wide-Long Format Reshaping**: Transform the JSON edit records from wide format (columns per language) to long format (language, edits).
4. **Interpolation and Imputation**: When parsing the JSON, treat any `null` edit values (or missing language keys compared to other records) as `0` edits.
5. **Resampling and Gap-filling**: Aggregate both views and edits per day, per language. If a language has views but no edits on a given day, edits should be `0`, and vice versa. 

**Output Requirements**:
The final output must be written to `/home/user/workspace/loc_daily_metrics.csv` with the following strict requirements:
- Columns: `date,lang,total_views,total_edits`
- Sorted chronologically by `date` (ascending), then alphabetically by `lang` (ascending).
- The `date` must be formatted as `YYYY-MM-DD`.
- Missing aggregates for a day/lang combination present in *either* file for that day must be `0`.

Run your Go program to generate the output file. You are restricted to Go standard library packages only.