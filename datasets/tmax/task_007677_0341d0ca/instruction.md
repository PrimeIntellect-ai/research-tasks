You are a DevOps engineer tasked with debugging a nightly log processing pipeline that has started failing. The pipeline reads server logs, enriches them with server metadata from a local SQLite database, and outputs an aggregated JSON summary. 

The pipeline is located in `/home/user/log_pipeline/`.

You need to resolve several issues to get the pipeline working correctly:

1. **Dependency Conflict:** The project uses a virtual environment, but running `pip install -r /home/user/log_pipeline/requirements.txt` currently fails due to a version conflict between `requests` and `urllib3`. Identify the conflict and fix `requirements.txt` so the dependencies install successfully. (Install them in a virtual environment at `/home/user/log_pipeline/venv`).
2. **Corrupted Input Handling:** The upstream log generator occasionally truncates lines or writes invalid UTF-8 characters. The main script `/home/user/log_pipeline/process_logs.py` currently crashes when it encounters these corrupted JSON lines in `/home/user/log_pipeline/data/raw_logs.jsonl`. Modify the script to gracefully skip any lines that cannot be parsed as valid JSON, continuing processing for the rest of the file.
3. **Query Result Debugging:** Even when the script runs, the output data is incorrect. The script queries a local SQLite database (`/home/user/log_pipeline/data/metadata.db`) to map server IPs to their physical regions. A bug in the SQL query causes a Cartesian product (cross join), assigning every region to every server and massively inflating the error counts. Fix the SQL query in `process_logs.py` so it correctly joins the `servers` and `regions` tables on `region_id`.

Once you have fixed the dependencies, the corrupted input handling, and the SQL query, run the pipeline script using your virtual environment:
`/home/user/log_pipeline/venv/bin/python /home/user/log_pipeline/process_logs.py`

This should generate the final output file at `/home/user/log_pipeline/output/summary.json`.

**Success Criteria:**
- The script must run without throwing exceptions.
- The `/home/user/log_pipeline/output/summary.json` file must be successfully created.
- The `summary.json` must contain the exact, correct aggregated error counts per region, formatted as a dictionary mapping region names (strings) to error counts (integers).