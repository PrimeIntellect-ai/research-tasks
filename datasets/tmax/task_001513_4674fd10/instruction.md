You are tasked with building a real-time data ingestion and aggregation service for an analytics pipeline. As part of this, you must fix a broken third-party C++ parsing library, build an HTTP service to compute rolling statistics, and bulk-export the processed data.

**Phase 1: Fix the Vendored JSON Parser**
You have been provided with a local copy of `libjsonparse-1.2` located at `/app/vendored/libjsonparse-1.2/`. 
This library is used for high-performance JSON-lines parsing. However, it currently contains a bug: it fails and throws an error when it encounters standard Unicode escape sequences (e.g., `\u00e9`) in JSON strings.
1. Inspect and fix the C++ code in `/app/vendored/libjsonparse-1.2/src/decoder.cpp` so it correctly processes (or safely ignores without crashing) standard unicode escapes.
2. Fix the `Makefile` in the same directory, which currently has a syntax error preventing compilation.
3. Compile the library and produce `libjsonparse.a`.

**Phase 2: Build the Data Aggregation Service**
Write a C++ HTTP server (you may use lightweight libraries like `cpp-httplib` by downloading the single header) that uses your fixed `libjsonparse.a` to process streaming data. 
Your server must:
1. Listen on `127.0.0.1:8080`.
2. Implement `POST /ingest`: Accepts a JSON-lines payload in the body. Each line will be a JSON object like: `{"timestamp": 1700000000, "value": 45.5, "event_name": "caf\u00e9_sale"}`. 
   - Parse each line using `libjsonparse`. 
   - Keep a running window of the last 10 successfully parsed `value` fields.
3. Implement `GET /rolling_stats`: Returns an HTTP 200 response with a JSON payload containing the average of the `value` field for the last 10 ingested records (or fewer, if less than 10 have been ingested). Format exactly: `{"rolling_avg": 45.5}`.
4. Implement `POST /export`: Flushes all successfully parsed records from memory into an SQLite database located at `/home/user/analytics.db`. Use a table named `events` with columns `timestamp INTEGER, value REAL, event_name TEXT`. You must use a bulk INSERT operation for efficiency.

**Constraints:**
- Do not use root privileges.
- Ensure the server stays running in the background or terminal so the automated verifier can test it.
- Your HTTP server must be able to handle standard JSONL payloads encoded in UTF-8.