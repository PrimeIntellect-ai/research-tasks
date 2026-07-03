You are a Database Reliability Engineer (DBRE) investigating a series of backup anomalies and securing our internal query API. 

We have three specific objectives:

1. **Video Log Extraction:** Our legacy backup appliance outputs its monitoring status as a video file. The file is located at `/app/backup_monitor.mp4`. You need to perform per-frame analysis to find out how many backup failures occurred. A backup failure is indicated by a completely black frame (average pixel brightness < 5 out of 255). Extract the frames using `ffmpeg` and write a Python script `analyze_frames.py` to count these failures. Output the final count to `/home/user/failure_count.txt`.

2. **Query Construction:** Write a Python script `/home/user/build_query.py` that contains a function `get_anomaly_query(table_name: str) -> str`. This function must return a valid, parameterized SQL (SQLite) query using window functions. The query should calculate the rolling average of `backup_size_mb` over the preceding 5 backups for each `db_name` in the given table, and return rows where the current backup is greater than 200% of its rolling average. Ensure the output schema maps to: `backup_id`, `db_name`, `backup_size_mb`, `rolling_avg`.

3. **Query Sanitization (Adversarial Corpus Verification):** Our internal API allows engineers to submit dynamic filter snippets (e.g., `db_name = 'user_db' AND backup_size_mb > 100`). We are experiencing SQL injection attempts. Write a script `/home/user/sanitizer.py` with a function `is_safe_filter(filter_string: str) -> bool`. 
   - We will test your function against two directories: `/app/corpus/clean/` (containing valid filters) and `/app/corpus/evil/` (containing SQL injection attempts, subqueries, and unauthorized DROP/ALTER commands).
   - Your function must return `True` for all clean filters and `False` for all evil filters.
   - Run your own tests. The automated grading will import your function and pass 100% of the corpus through it.

Save all files in `/home/user/`. Do not assume root privileges. Use Python built-in libraries where possible, though `Pillow` or `OpenCV` (if installed) can be used for frame analysis.