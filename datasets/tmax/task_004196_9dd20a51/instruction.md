You are tasked with fixing a broken internal data processing library and building a small ETL service that uses it to process incoming CSV data, handle encodings, normalize text, and aggregate records.

Your goal is to bring up an HTTP REST API server that acts as a webhook for an upstream ETL system. The upstream system sometimes retries failed batches, leading to duplicate records in the CSV payload.

Requirements:
1. **Fix and Install the Vendored Library**:
   You have been provided with an internal Python package located at `/app/vendor/csv-time-bucketer-1.2.0`. The package has a known issue in its configuration or code that prevents it from installing. Identify the issue, fix it, and install the package in your environment.
   The package provides a module `csv_time_bucketer` with a function `bucket_by_hour(records: list[dict], time_key: str) -> dict`.

2. **Develop the ETL Webhook Service**:
   Write and start a web server (e.g., in Python using Flask, FastAPI, or standard library) that listens on `127.0.0.1:9090`.
   It must expose a single endpoint: `POST /etl/process`.

3. **Authentication**:
   The endpoint must require an HTTP header: `X-API-Key: etl-secret-key-998`.
   If the header is missing or incorrect, return a `401 Unauthorized` status code.

4. **Payload Decoding and Parsing**:
   The endpoint will receive raw CSV data in the request body. The encoding of the payload will be specified in the `Content-Type` header (e.g., `Content-Type: text/csv; charset=iso-8859-1` or `charset=utf-16le`). Your server must correctly decode the payload using the specified charset.
   The CSV will always contain three columns: `record_id`, `event_time`, and `message`.

5. **Deduplication and Normalization**:
   Before bucketing, you must clean the data:
   - **Deduplication**: Due to retries, a `record_id` may appear multiple times. You must keep *only* the record with the most recent `event_time` for each `record_id`. (Assume `event_time` is always in ISO 8601 format and safely string-comparable/sortable).
   - **Tokenization/Normalization**: For the `message` field of the deduplicated records, convert all characters to lowercase. Replace any sequence of multiple whitespace characters (spaces, tabs, newlines) with a single space. Strip any leading or trailing whitespace.

6. **Aggregation**:
   Use the `bucket_by_hour` function from the installed `csv_time_bucketer` package to group the cleaned list of record dictionaries. Pass `'event_time'` as the `time_key`.

7. **Response**:
   Return a JSON response with status `200 OK` containing the exact dictionary returned by `bucket_by_hour`. The response should have the content type `application/json`.

Leave your server running in the foreground or background so it can be tested. Once your server is up and listening on `127.0.0.1:9090`, you consider the task complete.