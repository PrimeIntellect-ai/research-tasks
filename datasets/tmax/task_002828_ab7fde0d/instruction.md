Can you help fix our mobile build pipeline's artifact validation service? 

We have a two-tier microservice setup located in `/home/user/app/` that verifies mobile build manifests before signing them. 
1. **API Gateway (`api.py`)**: A Python Flask web service that should listen on `127.0.0.1:8080`. It receives JSON manifests via HTTP POST on the `/validate` endpoint.
2. **Validator Engine (`validator`)**: A legacy compiled binary that performs the actual cryptographic checks. It runs as a TCP service on `127.0.0.1:9090`.

Currently, the `api.py` service is failing to communicate properly with the `validator` backend. The Flask app correctly parses the incoming JSON, but the binary serialization in the `serialize_manifest()` function is incorrect, causing the `validator` to immediately drop the connection or return an error.

Your tasks:
1. Analyze the provided `validator.asm` (the x86_64 assembly source of the backend binary's parsing function) located in `/home/user/app/validator.asm` to understand the precise binary layout it expects.
2. Fix the `serialize_manifest()` function in `/home/user/app/api.py` so that it correctly packs the JSON data into the exact binary structure required by the assembly code (paying attention to magic bytes, endianness, field sizes, and padding).
3. Start the validator service in the background on port 9090 using:
   `socat TCP-LISTEN:9090,fork,reuseaddr EXEC:/home/user/app/validator &`
4. Start the API gateway in the background on port 8080 using:
   `python3 /home/user/app/api.py &`

The API gateway must successfully accept an HTTP POST to `http://127.0.0.1:8080/validate` containing a JSON payload like `{"version_code": 105, "is_debug": 1}`, forward the corrected binary payload to the validator, and return the HTTP 200 response with `{"status": "VALID"}`.

Please make the necessary code changes and leave both services running in the background so our integration test suite can verify the endpoint.