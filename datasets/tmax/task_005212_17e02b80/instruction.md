I've inherited a brittle, undocumented data ingestion pipeline. It consists of three services that start via a script `/app/start_services.sh`:
1. A Python Flask API on port 8001 (receives JSON payloads).
2. A local Redis instance on port 6379 (message queue).
3. A Ruby worker process (listens to Redis and writes to `/tmp/processed_logs.txt`).

Recently, the Ruby worker has been crashing or hanging when processing specific incoming payloads, bringing down the whole pipeline. I have isolated some data dumps. In `/home/user/data/clean/`, there are 50 JSON payloads that process perfectly. In `/home/user/data/evil/`, there are 50 JSON payloads that cause the worker to crash due to deeply nested malicious structures and corrupted unicode escapes (I'm not exactly sure what the precise trigger is, you'll need to figure out the delta between the clean and evil files).

Your task is to:
1. Diagnose the exact corrupted structure crashing the Ruby worker by analyzing and delta-debugging the inputs.
2. Create a standalone multi-language compatible validation script at `/home/user/validator.py`. This script must accept a file path as its first CLI argument, read the JSON file, and print "ACCEPT" to stdout with exit code 0 if the payload is safe, or print "REJECT" to stdout with exit code 1 if it contains the corruption.
3. Reconfigure the Python Flask API (source located at `/app/api/app.py`) to shell out to `/home/user/validator.py` for every incoming request. If the validator rejects it, the API should return a 400 status code and drop the payload, rather than pushing it to Redis. 
4. Ensure the full multi-service pipeline runs successfully end-to-end so that `curl -X POST -H "Content-Type: application/json" -d @<file> http://localhost:8001/ingest` works cleanly for good files and correctly rejects bad files without crashing the Ruby worker.

Leave the services running when you are finished. Automated tests will verify your validator against a hidden set of evil and clean corpora, and will test the end-to-end pipeline through port 8001.