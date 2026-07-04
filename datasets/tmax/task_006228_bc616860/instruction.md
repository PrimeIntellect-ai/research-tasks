You are an AI assistant helping a data scientist clean a dataset of customer feedback. 

We have a batch of JSON-lines (`.jsonl`) files located in `/home/user/raw_data/`. These contain raw customer feedback. Unfortunately, some upstream system introduced malformed unicode escape sequences (e.g., `\u12G4` or truncated escapes) into a few records, causing standard JSON parsers to crash.

Your task is to build a robust, parallelized data processing pipeline to clean this data and load it into a database.

Please complete the following steps:

1. Write a Python script `/home/user/clean_data.py` to process these files:
   - Use Python's `multiprocessing` or `concurrent.futures` modules to process the `.jsonl` files in parallel.
   - Read each line of each file.
   - If a line parses successfully with standard `json.loads()`, extract the `id`, `user`, and `text` fields.
   - If a line fails to parse (e.g., throwing a `json.decoder.JSONDecodeError`), catch the exception and log the failure to `/home/user/pipeline_errors.log`. The log entries must exactly match this format:
     `[<filename>] Line <line_number>: <raw_line_content>`
     (Note: line numbers should start at 1 for each file. `<filename>` should be just the basename of the file, e.g., `file2.jsonl`).
   - Use bulk SQLite operations (like `executemany`) to insert all successfully parsed records into an SQLite database at `/home/user/cleaned_data.db`.
   - The database should have a table named `feedback` with three columns: `id` (TEXT), `user` (TEXT), and `text` (TEXT). Your script should create this table if it does not exist.

2. Create a bash wrapper script `/home/user/run_job.sh`:
   - This script should simply execute the Python script you wrote.
   - Ensure it has execute permissions.

3. Schedule the pipeline:
   - Create a cron schedule file at `/home/user/schedule.cron`.
   - Write a valid crontab entry in this file that schedules `/home/user/run_job.sh` to run every day at exactly 2:30 AM.

Run your script once manually (via the wrapper script) to process the current data in `/home/user/raw_data/` and populate the database and error log.