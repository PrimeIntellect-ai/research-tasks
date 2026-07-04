You are a data engineer responsible for building an automated text processing ETL pipeline. 

You have two datasets:
1. `/home/user/data/users.csv` with columns: `user_id,region,account_type`
2. `/home/user/data/messages.csv` with columns: `msg_id,user_id,timestamp,message_text`

Your objective is to write a Python script at `/home/user/etl_pipeline.py` that performs the following:
1. **Validation:** Read `messages.csv`. Filter out (drop) any rows where `message_text` is completely empty or contains only whitespace. Also filter out rows where the `timestamp` does not strictly match the format `YYYY-MM-DD HH:MM:SS` (e.g., `2023-10-01 14:30:00`).
2. **Join/Merge:** Join the validated messages with `users.csv` on the `user_id` column.
3. **Parallel Text Processing:** Use Python's `multiprocessing` module (e.g., `Pool`) to calculate the word count for the `message_text` of each valid row in parallel. Words are separated by whitespace.
4. **Aggregation:** Calculate the average word count per `region`.
5. **Output:** Save the aggregated summary statistics as a JSON file at `/home/user/output/region_stats.json`. The keys should be the region names, and the values should be the average word count as a float, rounded to exactly 2 decimal places.

Additionally, you must schedule this pipeline to run every day at 2:00 AM:
1. Create a cron job for the `user` user that runs `python3 /home/user/etl_pipeline.py`.
2. Save a copy of the active crontab to `/home/user/cron_backup.txt` using `crontab -l > /home/user/cron_backup.txt`.

Constraints & Setup:
- Assume the data directories `/home/user/data/` and `/home/user/output/` exist.
- Use standard library modules or `pandas` (which is installed).