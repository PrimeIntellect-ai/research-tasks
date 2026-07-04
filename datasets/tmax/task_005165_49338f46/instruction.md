You are an AI assistant helping a data scientist automate a data cleaning pipeline.

We have a pipe-separated data file located at `/home/user/raw.dat`. Each line represents a sensor reading in the format `timestamp|sensor_id|reading` (e.g., `162060|S2|45.0`).

Your task is to write a bash script at `/home/user/pipeline.sh` that does the following when executed:
1. Calculates the mathematical mean (average) of all the `reading` values in `/home/user/raw.dat`.
2. Filters the data to keep only the rows where the `reading` is strictly greater than this mean.
3. Converts the filtered rows from pipe-separated (`|`) to comma-separated (`csv`) format.
4. Saves this cleaned, comma-separated data to `/home/user/filtered.csv`.
5. Creates an SQLite database at `/home/user/sensors.db` with a table named `valid_readings` (columns: `timestamp INTEGER`, `sensor_id TEXT`, `reading REAL`).
6. Bulk imports the data from `/home/user/filtered.csv` into the `valid_readings` table.

After writing the script:
- Make sure `/home/user/pipeline.sh` is executable.
- Execute the script once so the database is populated.
- Set up a cron job for the current user (`user`) that schedules `/home/user/pipeline.sh` to run exactly at the top of every hour (e.g., 01:00, 02:00, etc.).

Ensure you only use standard Bash utilities (like `awk`, `sed`, `sqlite3`, etc.). Do not use Python or other scripting languages for this specific task.