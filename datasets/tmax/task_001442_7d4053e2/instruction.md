You are a mobile build engineer tasked with maintaining a data processing pipeline that feeds telemetry data into our backend.

We have a multi-service local backend for testing, consisting of:
1. An Nginx reverse proxy running on port 8080.
2. A Python Flask API.
3. A Redis cache.

Currently, the pipeline consists of a Rust CLI tool (`/home/user/telemetry_fmt`) that formats raw telemetry strings, and a Python orchestrator that submits them. However, the system is broken and too slow:
1. The Rust tool currently fails to compile due to ownership and borrow checker errors.
2. We need a Python script `/home/user/submit_telemetry.py` that reads 50,000 lines of raw telemetry from `/home/user/raw_telemetry.txt`, processes them using the Rust tool, and uploads them to the local API.

Your tasks:
1. **Fix the Rust tool**: Navigate to `/home/user/telemetry_fmt` and fix the borrow checker issue in `src/main.rs`. The tool should take newline-separated strings via standard input, prepend `MOBILE_V1:` to each string, and output the result to standard output. Build it in release mode.
2. **Configure the services**: The services are provided in `/app/services`. You must start them. Nginx should be configured to proxy requests on `http://localhost:8080` to the Flask app on `127.0.0.1:5000`. 
3. **Write the Python Orchestrator**: Create `/home/user/submit_telemetry.py` to process the data. To meet our strict performance requirements, your Python script must run in under 2.5 seconds. Calling the Rust binary 50,000 times individually will be too slow; you should pass the data to the Rust tool in a single batch via stdin/stdout. Then, submit the processed lines to the backend via an HTTP POST request to `http://localhost:8080/api/batch`. The payload must be JSON in the format: `{"telemetry": ["MOBILE_V1:line1", "MOBILE_V1:line2", ...]}`.

Constraints:
- You must use Python for `submit_telemetry.py`.
- The total execution time of `submit_telemetry.py` must be strictly less than 2.5 seconds (metric threshold).
- Ensure the services (Redis, Flask, Nginx) are running correctly before running your script.
- Write a bash script `/home/user/run_all.sh` that compiles the Rust tool, starts the services, and runs the Python script.