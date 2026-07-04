You are an operations engineer triaging an incident with a new log-ingestion pipeline. 

The pipeline is located in `/home/user/app/` and consists of three components:
1. A Flask API (`api.py`) that receives raw text logs via HTTP POST on port 8080.
2. A Redis instance acting as a message broker.
3. A Python worker (`worker.py`) that pulls logs from Redis, parses them, and appends valid JSON objects to `/home/user/app/parsed_logs.json`.

Currently, the pipeline is completely broken:
- **Routing Issue**: When you start the services using `/home/user/app/start.sh`, sending a log to the API returns a 200 OK, but the worker never sees it. You need to fix the configurations or startup scripts so the end-to-end flow works.
- **Parsing Bug**: The core parsing logic in `/home/user/app/parser.py` (used by the worker) is notoriously brittle. It crashes or outputs malformed data when encountering corrupted input logs (which are common in our environment). 

Your objective is to fix both the pipeline configuration and the parsing logic. 

To ensure the parsing logic is perfectly robust, you must make `parser.py` behave **exactly** like our legacy C-based parser, which is available as an oracle binary at `/home/user/oracle/parser_oracle`.
The oracle takes a raw log string via `stdin` and outputs a specific JSON format to `stdout` (or `{"error": "invalid format"}` for unrecoverable corruptions). 
You must modify `/home/user/app/parser.py` so that when it is executed as a script (reading from `stdin`), its stdout output is bit-for-bit identical to the oracle's output for ANY given input string, including highly corrupted edge cases.

**Requirements:**
1. Fix the environment/service configuration so that an HTTP POST to `http://localhost:8080/ingest` with `{"raw_log": "..."}` results in the parsed JSON appearing in `/home/user/app/parsed_logs.json`.
2. Fix `parser.py` so it perfectly mirrors `/home/user/oracle/parser_oracle` for all inputs. Do not hardcode solutions; the automated tests will fuzz your parser with thousands of random, corrupted log lines.