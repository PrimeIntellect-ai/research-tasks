You are acting as a Release Manager preparing the final deployment pipeline for a new analytics ingestion system. The deployment involves orchestrating a polyglot microservice architecture, migrating legacy data, and setting up cross-language bindings.

The system is located in `/home/user/app/` and consists of two primary services:
1. **Ingestion API**: A Python Flask service that receives analytics events via HTTP.
2. **Analyzer Backend**: A high-performance C-based engine wrapped in a Python TCP server.

Currently, the system is incomplete and cannot be deployed. You need to perform the following steps to finalize the deployment:

**Step 1: Polyglot Build & FFI Setup**
In `/home/user/app/backend/`, there is a C source file `analyzer.c`. 
- Compile it into a shared library named `libanalyzer.so` in the same directory.
- Open `/home/user/app/backend/backend_tcp.py`. This script starts a TCP server on port 9090, but the FFI integration is missing. Using `ctypes`, define the `AnalyticsPayload` struct to match the C implementation and complete the `process_payload` function so it successfully calls the `compute_risk_score` function from `libanalyzer.so`.

**Step 2: Code Translation & Validation**
The Ingestion API must validate incoming payloads before sending them to the backend. The validation logic was previously written in Node.js and is located at `/home/user/app/api/legacy_validate.js`.
- Translate this exact validation logic into Python.
- Integrate it into `/home/user/app/api/ingest_api.py` in the `/ingest` endpoint handler. If validation fails, the API must return an HTTP 400 response with `{"error": "Validation failed"}`.

**Step 3: Schema Migration**
The backend records historical trends in an SQLite database located at `/home/user/app/data/analytics.db`. 
- The `events` table currently uses an integer `timestamp` column.
- Write and execute a schema migration that adds a new column `iso_time` (TEXT) to the `events` table.
- Backfill the `iso_time` column by converting all existing UNIX timestamps in the `timestamp` column to ISO 8601 string format (e.g., `2023-10-05T14:48:00Z`).
- Drop the old `timestamp` column and rename `iso_time` to `timestamp` (note: SQLite requires a table recreation pattern for this).

**Step 4: Service Orchestration**
Once the above is complete, start both services in the background:
- `backend_tcp.py` must listen on `127.0.0.1:9090` (raw TCP).
- `ingest_api.py` must listen on `127.0.0.1:8080` (HTTP).

Ensure both services are running and functioning properly. A verification script will test the full end-to-end flow by sending HTTP POST requests to the Ingestion API and verifying the C-computed risk scores.