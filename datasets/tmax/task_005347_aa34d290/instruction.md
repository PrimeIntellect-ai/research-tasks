You are a log analyst investigating patterns in an e-commerce platform's traffic. Recently, our compliance team mandated that all logs must be anonymized before they are stored in our central analytics database. We have a multi-service setup but the ETL pipeline connecting them is missing.

Currently running on the system (in `/app/`):
1. A Redis server (localhost:6379)
2. A Log Generator service that continuously pushes raw log strings to a Redis list called `raw_logs`.
3. A Flask Ingestion API (localhost:5000) with a `POST /ingest` endpoint that expects a JSON payload: `{"logs": ["log_string_1", "log_string_2", ...]}`.

Your task is to build and orchestrate an ETL pipeline to process these logs:

1. **Data Masking (Python)**: Write a script `/home/user/pipeline.py` that pops up to 100 logs from the Redis list `raw_logs` (using `LPOP`). For each log string, you must anonymize sensitive information using regex:
   - **Emails**: Mask the local part but keep the domain. (e.g., `john.doe@example.com` -> `[MASKED]@example.com`).
   - **Credit Cards**: Mask the first 12 digits of a 16-digit card number separated by dashes. (e.g., `1234-5678-9012-3456` -> `XXXX-XXXX-XXXX-3456`).
   - **IPv4 Addresses**: Mask the final octet. (e.g., `192.168.1.150` -> `192.168.1.XXX`).
   
2. **Integration**: The script must then send the masked logs to the Flask API at `http://localhost:5000/ingest` using a POST request.

3. **Orchestration**: Write a scheduler script `/home/user/orchestrator.py` that runs `pipeline.py` continuously, sleeping for 1 second between runs. Ensure it runs in the background.

To successfully complete the task, you must start your orchestrator and let it run. The automated verifier will analyze the data ingested by the Flask API to calculate a masking accuracy metric. You need an F1-score of at least 0.95 (meaning you accurately masked PII without accidentally destroying non-PII log metadata like timestamps or URLs).