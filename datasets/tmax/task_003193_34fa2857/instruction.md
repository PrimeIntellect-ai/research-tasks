You are a Database Reliability Engineer (DBRE) investigating a complex backup chain failure. 

The on-call manager left an emergency voice memo detailing the incident and the exact criteria needed to generate a diagnostic report. The audio file is located at `/app/voicemail.wav`.

Your task is to:
1. Transcribe the audio file to understand the required query criteria.
2. Analyze the SQLite database at `/home/user/backups.db`. The database contains a single table: `backup_jobs (job_id INTEGER PRIMARY KEY, parent_job_id INTEGER, region TEXT, status TEXT, size_bytes INTEGER, start_time DATETIME)`.
3. Write a Python script at `/home/user/analyze.py` that:
   - Connects to the database.
   - Creates necessary indexes to optimize the recursive operations requested (the table contains over 200,000 rows, and an unoptimized recursive query will timeout).
   - Executes the complex SQL query using the criteria specified in the voicemail (combining recursive CTEs, window functions, and pagination/filtering).
   - Exports the final result set to a CSV file at `/home/user/report.csv` with headers matching the selected columns.

Ensure your Python script runs without user intervention and completes the execution efficiently. You may use any transcription tool available (like `whisper` or `ffmpeg` to process the audio) to extract the instructions first.