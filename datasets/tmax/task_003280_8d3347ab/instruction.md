You are an automation specialist tasked with modernizing a legacy ETL workflow. We have a compiled, stripped legacy binary at `/app/legacy_etl` that converts CSV data into JSON. However, it has a known bug: it frequently simulates "retries" internally and outputs duplicate JSON records.

Your goal is to build a Python-based pipeline orchestration and data masking service that wraps this binary, cleans its output, and serves the results over an HTTP API.

Here are the requirements:

1. **The Legacy Binary**: 
   - Path: `/app/legacy_etl`
   - Usage: It reads CSV data from `stdin` and writes a stream of JSON objects (one per line) to `stdout`.
   - The binary occasionally duplicates records. 

2. **Data Pipeline Requirements**:
   - Write a Python script to orchestrate this process.
   - You must read an input CSV file (which will be provided via the API).
   - Pass the CSV data to the binary.
   - Deduplicate the resulting JSON records based on the `record_id` field (keep the first occurrence).
   - **Data Masking**:
     - Mask the `ssn` field: Replace the first 5 digits with asterisks (e.g., `123-45-6789` becomes `***-**-6789`). Use regex for this.
     - Mask the `email` field: Keep the first character and the domain, replace all other characters in the local part with a single `*` (e.g., `john.doe@example.com` becomes `j*@example.com`).

3. **HTTP Service**:
   - The Python script must start an HTTP server listening exactly on `127.0.0.1:9090`.
   - Endpoint 1: `GET /health` - Must return HTTP 200 with JSON payload `{"status": "ok"}`.
   - Endpoint 2: `POST /process` - Will receive the raw CSV data in the request body (text/csv). It must run the pipeline (pass the body to the binary, deduplicate, mask) and return a JSON array of the processed, deduplicated, and masked records.

Write the complete Python service and start it. Ensure it remains running in the foreground or background so the automated verifier can test the endpoints. You may use standard Python libraries or install frameworks like Flask/FastAPI.