You are a backup administrator tasked with securing and archiving system logs in a multi-service environment. We have an architecture consisting of three components:
1. A log generator service that writes multi-line application logs to `/home/user/app/logs/raw/`.
2. A Redis instance acting as a metadata store for processed files.
3. An archiving worker (which you must implement).

Your task has two main parts:

**Part 1: Implement the Log Sanitizer & Archiver**
Write a Python script at `/home/user/archiver.py` that contains a specific function: `def sanitize_and_archive(input_log_path: str, output_archive_path: str) -> bool:`
- The function must read the multi-line log file at `input_log_path`.
- It must detect and redact sensitive information (Credit Card numbers and RSA private key blocks). Replace CC numbers (16 digits, with or without dashes) with `[REDACTED_CC]`. Replace any multi-line RSA private key block with `[REDACTED_KEY]`.
- If the log is completely corrupted (starts with invalid binary headers instead of text), the function must return `False` and drop the file.
- If successful, it must write the sanitized logs into a compressed `.tar.gz` archive at `output_archive_path` containing the text file, and return `True`.
- Your script should also include a CLI entry point: `python /home/user/archiver.py --input <path> --output <archive_path>`.

**Part 2: Multi-Service Integration**
The services are defined in `/home/user/app/docker-compose.yml` (Redis on port 6379, LogGen on port 8080). 
- Modify `/home/user/app/config.ini` so that the `archiver_cmd` points exactly to your Python script entrypoint.
- Write a bash script at `/home/user/start_pipeline.sh` that starts the docker-compose services in the background, waits 5 seconds, and then runs a continuous file-watching loop using `inotifywait` on `/home/user/app/logs/raw/`. Whenever a new log is closed-written, it should pipe the file path to your archiver script, saving the output to `/home/user/app/logs/archives/`, and then record the successful archive name in Redis (using `redis-cli LPUSH archived_logs <filename>`).

Ensure the pipeline successfully processes the standard logs without crashing, and that your sanitizer is robust. We will test your `archiver.py` independently against a corpus of clean and evil log files.