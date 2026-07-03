You are a data scientist tasked with fixing and deploying a streaming data cleaning pipeline. The pipeline ingests JSON-lines telemetry data containing statistical probability distributions, buffers it, and cleans it. 

The system uses three services: Nginx, a Flask Ingestion API, and Redis.
Currently, the services are provided in `/workspace/system/`, but they are misconfigured and the cleaning worker is missing.

Your objectives:

1. **Service Composition & Configuration:**
   - Fix `/workspace/system/nginx.conf` so that Nginx (listening on port 8080) correctly reverse-proxies requests from `/ingest` to the Flask app running on `127.0.0.1:5000`.
   - Start Nginx, Redis (default port 6379), and the Flask app (`python /workspace/system/flask_app.py`).

2. **Data Sanitization & Validation (The Worker):**
   - Write a Python script at `/workspace/worker.py` that continuously pops JSON-lines strings from the Redis list `raw_data` (using `BLPOP` or similar).
   - The JSON strings contain records with the schema: `{"id": int, "group": str, "probabilities": [float, ...], "value": float}`.
   - **Unicode Issue:** The incoming JSON-lines often contain broken, unescaped unicode sequences (e.g., raw `\u` without the hex digits) that crash standard parsers. Your worker must sanitise these strings before parsing (e.g., stripping invalid unicode escapes) without discarding the whole line if the rest is valid.
   - **Math Constraints:** You must validate the parsed data. Reject (ignore) records if:
     a) The `probabilities` array does not sum to 1.0 (allow a tolerance of 1e-5).
     b) `value` is strictly negative.
   - Valid records must be serialized back to JSON and pushed to the Redis list `clean_data`.

3. **Sampling & Template Generation:**
   - As your worker processes valid records, maintain a stratified sample: keep exactly the first 2 valid records for each unique `group`.
   - Whenever a new valid record is added to the sample, regenerate an HTML report at `/workspace/report.html` using a template. The HTML must precisely match this format:
     ```html
     <html><body>
     <h1>Sampled IDs</h1>
     <ul>
     <li>Group A: id1, id2</li>
     <li>Group B: id3</li>
     </ul>
     </body></html>
     ```
     (Groups must be sorted alphabetically, and IDs within them ordered by appearance).

You can test your worker using the corpora in `/workspace/data/`. The automated test will push `/workspace/data/clean.jsonl` and `/workspace/data/evil.jsonl` through Nginx (`POST http://127.0.0.1:8080/ingest`) and verify that exactly 100% of the clean records appear in Redis `clean_data` and 100% of the evil records are rejected.