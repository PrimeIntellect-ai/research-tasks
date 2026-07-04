You are a data engineer tasked with migrating and serving data from a legacy system. We have a set of raw text files, a legacy C binary that performs our proprietary text normalization, and a reference mapping file. 

Your goal is to build an ETL pipeline in Python (orchestrated via a bash script if you prefer, but the logic and server must be in Python) that processes this data, aggregates it, joins it with reference data, logs its progress, and ultimately serves the aggregated metrics via an HTTP API.

Here are the exact requirements:

1. **Environment & Files**:
   - Raw input data is located at: `/home/user/etl_project/data/raw/` (contains multiple `.txt` files).
   - Reference mapping file: `/home/user/etl_project/data/reference.csv` (CSV format: `normalized_word,category`).
   - Legacy normalizer binary: `/home/user/etl_project/bin/legacy_norm` (This is a stripped, compiled binary. It takes raw text from `stdin` and outputs normalized space-separated tokens to `stdout`).

2. **ETL Pipeline Steps**:
   - **Extract & Normalize**: Read all `.txt` files in the raw data directory. Pass their contents through the `/home/user/etl_project/bin/legacy_norm` binary.
   - **Aggregate (Sort & Group)**: Count the total frequency of each normalized word across all documents.
   - **Merge**: Join your aggregated word counts with the `reference.csv` file to calculate the total word count per *category*. If a word is not in the reference file, categorize it as `"UNKNOWN"`.
   - **Log**: Throughout the process, write structured JSON logs to `/home/user/etl_project/logs/etl.log`. You must log at least three events with the format `{"step": "<step_name>", "status": "completed", "records": <count>}` for the extract, aggregate, and merge steps.

3. **Serving (Multi-Protocol)**:
   - Once the ETL pipeline completes and the data is aggregated in memory (or saved to a local SQLite/JSON file), your Python script must start a persistent HTTP web server listening exactly on `127.0.0.1:9000`.
   - The server must expose a single HTTP GET endpoint: `/api/stats?category=<category_name>`
   - The endpoint must return a JSON response in the exact format: `{"category": "<category_name>", "total_count": <integer_sum>}`.
   - Return a 404 HTTP status code if the category does not exist in your aggregated results.

Write the code, execute the pipeline, and leave the HTTP server running in the background so the automated verification system can test it.