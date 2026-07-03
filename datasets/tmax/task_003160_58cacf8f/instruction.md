You are a support engineer investigating a severe stability issue in our data ingestion pipeline. Our downstream backend service simulates a strict Rust analytics engine that routinely panics (crashes) when it encounters specific edge-case telemetry data.

The system consists of three cooperating services running locally:
1. **NGINX Reverse Proxy** (listening on port 8080)
2. **Python Ingestion Service** (listening on port 5000)
3. **Backend Analytics Engine** (listening on port 5001)

When you run `/home/user/start_services.sh`, all three services will start. However, when certain "poison pill" JSON payloads are sent to `http://localhost:8080/ingest`, the Backend Analytics Engine crashes and must be restarted. 

Through intermediate state tracing, we have gathered a set of diagnostic payloads. You have two directories:
- `/home/user/corpora/clean/` - Contains 50 normal JSON payloads that the backend processes successfully.
- `/home/user/corpora/evil/` - Contains 50 malformed JSON payloads that cause the backend to crash.

Your tasks:
1. **Analyze the Failures**: Inspect the logs and the corpora to determine the root cause of the crashes. Look closely at floating-point values and string encodings.
2. **Build a Detector**: Create a Python script at `/home/user/detector.py`. 
   - It must take a single file path as a command-line argument.
   - It must read the JSON file and validate it.
   - If the file is "clean", it must exit with status code `0`.
   - If the file is "evil", it must exit with status code `1`.
3. **Patch the Pipeline**: Modify the ingestion service (`/home/user/services/ingestion.py`) to use your validation logic. It should return an HTTP 400 response for evil payloads, preventing them from reaching the backend, while forwarding clean payloads to `http://localhost:5001/process`.

An automated verification suite will test your `detector.py` against hidden validation corpora and test the end-to-end system via NGINX. Do not attempt to modify the Backend Analytics Engine (`/home/user/services/backend.py`), as it represents a compiled binary in production.