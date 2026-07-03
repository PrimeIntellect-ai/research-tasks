You are an AI assistant helping a data scientist clean and process a large dataset of audio transcription logs. You need to write a highly efficient data processing pipeline in Go.

Our systems continuously generate transcription logs in JSONL format, but the data is noisy. Some logs are corrupted, contain invalid measurements, or include malicious injection strings from untrusted user audio. 

Additionally, a daily run ID is generated from an automated voice system. We have the raw audio recording of today's run ID at `/app/data/run_id.wav`.

Your task is to create a Go program that performs the following steps:

1. **Audio Processing**:
   The Go program must accept a `--audio` flag pointing to an audio file (e.g., `/app/data/run_id.wav`). The audio contains a spoken 4-digit number. You must transcribe this number (you may use any available terminal tools like `ffmpeg`, `python3`, or install lightweight transcription tools like `whisper-cpp` to find out what it says) and parse it as an integer. This integer will be used as the `run_id`.

2. **Stream Processing & Filtering (The Classifier)**:
   The program must read a continuous stream of JSONL logs from `stdin`. Each JSON object has the following schema:
   `{"id": "string", "timestamp": "int64", "duration_sec": "float64", "confidence": "float64", "transcript": "string"}`
   
   You must implement a filter that drops "evil" or invalid records. A record MUST be rejected (dropped completely) if ANY of the following are true:
   - `duration_sec` is less than or equal to 0.0.
   - `confidence` is outside the bounds of 0.0 to 1.0 (inclusive).
   - `transcript` contains the exact substrings `<script>`, `DROP TABLE`, or `DELETE FROM` (case-insensitive).
   - `transcript` is completely empty.

3. **Rolling Aggregation**:
   For the valid logs that pass the filter, you must calculate a rolling window average of the `confidence` score. The window size is the last 5 valid records (or fewer, if less than 5 records have been processed).

4. **Database Bulk Import**:
   The program must accept a `--db` flag pointing to a SQLite database file path.
   You must bulk insert the valid records into a SQLite table named `clean_logs`.
   The table schema must be:
   `id (TEXT PRIMARY KEY), timestamp (INTEGER), duration_sec (REAL), transcript (TEXT), confidence (REAL), rolling_avg_conf (REAL), run_id (INTEGER)`

Requirements:
- Your Go code must be written to `/home/user/cleaner.go` and compiled to `/home/user/cleaner`.
- Ensure your Go program is highly efficient, processing `stdin` in a streaming fashion rather than loading the entire input into memory.
- You must use `database/sql` and `github.com/mattn/go-sqlite3` for the database operations.
- Do not output any invalid records to the database.

To verify your work, I will pipe a large JSONL corpus into your program:
`cat /app/data/corpus.jsonl | /home/user/cleaner --audio /app/data/run_id.wav --db /home/user/output.db`