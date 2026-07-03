You are helping a data scientist clean a messy, unstructured log dataset. 

There is a log file located at `/home/user/messy_data.log`. The file is potentially very large, so we must process it efficiently without loading the entire file into memory at once.

Your task is to build a mini data processing pipeline with two components:

1. **Python Extractor (`/home/user/extract.py`)**:
Write a Python script that reads `/home/user/messy_data.log` line-by-line (streaming). 
Use regular expressions to extract timestamps and email addresses. 
- Timestamps are formatted exactly like `[YYYY-MM-DD HH:MM:SS]`.
- Email addresses are standard formats (e.g., `user@example.com`).
- Only process lines that contain exactly ONE timestamp and exactly ONE email address.
- The script should output the extracted data to `/home/user/extracted.csv` with the format `timestamp,email` (e.g., `2023-10-14 08:30:00,admin@server.local`). Do not include the brackets from the timestamp in the CSV.

2. **Pipeline Orchestrator (`/home/user/pipeline.sh`)**:
Write a bash script that acts as a simple pipeline DAG. It must:
- Run the `extract.py` script.
- Take the resulting `/home/user/extracted.csv`, sort it chronologically by the timestamp, remove any duplicate rows, and write the final output to `/home/user/clean_data.csv`.

Make sure `/home/user/pipeline.sh` is executable and run it to produce the final `clean_data.csv`.