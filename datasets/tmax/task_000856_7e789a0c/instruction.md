You are tasked with building a robust data processing worker for our real-time log ingestion pipeline. 

Our current architecture involves a Flask ingestion API and a Redis message broker. We need you to implement the worker that reads from the queue, rigorously sanitizes the payloads, and normalizes the output into a structured CSV file. The data contains PII (Personally Identifiable Information) and is susceptible to malformed inputs and adversarial payloads.

### System Architecture
1. **Redis**: Running locally on the default port `6379`.
2. **Ingestion API**: A Flask app running on port `8080`. It receives JSON-lines data via POST requests to `/ingest` and pushes raw byte strings to a Redis list named `data_queue`.

### Your Objectives

**1. Create the Data Sanitizer (`/home/user/sanitizer.py`)**
Write a Python module containing the function exactly matching this signature:
`def process_and_sanitize(raw_payload: bytes) -> dict | None:`

This function must perform the following:
* **Format Handling:** Safely decode the bytes and parse the JSON string. If the payload is malformed JSON or contains broken unicode escape sequences, catch the error and return `None`.
* **Constraint Validation:** The parsed dictionary must contain the keys: `user_id` (int), `email` (str), `ssn` (str), `age` (int), and `event_type` (str). If any keys are missing, or if `age` is less than 0 or greater than 120, return `None`.
* **Security & Cleaning:** If `event_type` contains any characters other than alphanumeric characters and underscores `_`, reject the payload by returning `None`.
* **Anonymization:** 
    * Replace the `ssn` value entirely with the string `XXX-XX-XXXX`.
    * Mask the `email` local part with `hidden`, preserving the domain (e.g., `alice.smith@company.com` becomes `hidden@company.com`).
* Return the sanitized dictionary if all checks pass.

**2. Create the Queue Worker (`/home/user/worker.py`)**
Write a Python script that continuously polls the Redis list `data_queue` (using blocking pop, e.g., `BLPOP`).
For every item retrieved:
* Pass the raw bytes to `process_and_sanitize`.
* If a valid sanitized dictionary is returned, append it as a row to a CSV file located at `/home/user/processed_logs.csv`.
* The CSV file must have exactly these headers in this order: `user_id,email,ssn,age,event_type`. 
* Ensure the CSV is created with headers if it does not exist, and subsequently appended to without duplicating the headers.
* Ensure data is flushed to disk immediately so automated tests can verify the output.

### Instructions
1. Install any necessary Python packages (e.g., `redis`) in your environment.
2. Implement `/home/user/sanitizer.py` and `/home/user/worker.py`.
3. Start your worker in the background (e.g., `python3 /home/user/worker.py &`). 
4. Leave the worker running so the testing suite can send payloads to the API and evaluate your system's end-to-end processing.