You are a log analyst investigating a recent series of server anomalies. You have been provided with two artifacts:
1. A corrupted server log file at `/app/raw_logs.csv`.
2. A screen recording of the server's physical alert dashboard at `/app/server_dashboard.mp4`.

Your objective is to clean the data, extract alert states from the video, compute necessary statistics, store the results in a database, and expose them via a REST API.

**Step 1: Video Alert Extraction**
The video `/app/server_dashboard.mp4` is exactly 10 seconds long (10 frames at 1 fps). Most of the time, the dashboard is black (pixel intensity near 0). During an alert, the dashboard flashes white (high average pixel intensity).
* Extract the frames at 1 frame per second.
* Calculate the average grayscale pixel intensity for each frame.
* If the average intensity is > 128, consider that second (0-indexed) to have `alert = 1`, otherwise `alert = 0`.

**Step 2: Log Cleaning & Data Validation**
The file `/app/raw_logs.csv` has the headers: `timestamp,ip_address,response_time,cpu_load`. (The timestamp corresponds to the seconds 0 through 9 matching the video).
* **Validation:** Filter out any rows where `ip_address` does not perfectly match a valid IPv4 address format.
* **Imputation:** The `cpu_load` column has missing values (empty strings). Impute these missing values using simple forward-fill (use the last known valid `cpu_load`). For the first row, if missing, use `0.0`.
* **Rolling Statistics:** Compute a 3-row rolling average of the `response_time` column (current row and the 2 preceding valid rows). For the first two rows, compute the average of the available rows.

**Step 3: Integration & Bulk Export**
Merge the cleaned log data with the video alert data based on the `timestamp` (0 to 9).
Write the final dataset to `/home/user/cleaned_logs.csv` with headers: `timestamp,ip_address,response_time,cpu_load,rolling_resp,alert`.
Bulk import this CSV into a SQLite database located at `/home/user/logs.db` in a table named `metrics`.

**Step 4: API Service**
Create and start a Python HTTP server listening on `127.0.0.1:8000`.
The API must support two endpoints:
* `GET /alerts` : Returns a JSON array of `timestamp` integers where `alert == 1`.
* `GET /stats` : Returns a JSON object mapping the `timestamp` (as a string) to its `rolling_resp` value (rounded to 2 decimal places).

The API must be running in the background so it can be queried. Do not exit your final script.