You are a data engineer debugging an ETL pipeline. A previous job processed a large dataset of events, but due to a silent type-coercion bug (similar to Pandas converting integers to floats when NaNs are introduced), the `user_id` column in our output has been corrupted. Some IDs are missing, some have been converted to scientific notation or floats (e.g., `NaN`, `1.0e6`, `1234.0`), and some remain valid integers.

Your task is to write a Go program to validate this data, handle the missing/outlier values, and produce a clean dataset for reproducible downstream use.

**Requirements:**
1. Create a Go program at `/home/user/clean_data.go`.
2. The program must read the CSV file located at `/home/user/data/events.csv`. The CSV has a header: `event_id,user_id,value`.
3. Process the file row by row:
   - If the `user_id` is perfectly empty (a missing value), **drop** the row silently.
   - If the `user_id` is a valid base-10 integer (e.g., `1042`, `0`, `-5`), **keep** the row and write it to `/home/user/data/cleaned.csv`.
   - If the `user_id` is anything else (e.g., `NaN`, `1.5e6`, `100.0`, `null`), treat it as an anomaly. **Write the `event_id`** of that anomalous row to `/home/user/anomalies.txt` (one `event_id` per line).
4. The file `/home/user/data/cleaned.csv` must include the original header row.
5. Compile and run your Go program to generate the output files. Ensure the output is deterministically reproducible.

Do not use any third-party Go libraries outside the standard library (e.g., `encoding/csv`, `os`, `strconv` are fine).