You are tasked with setting up the validation and routing layer for a new polyglot build system. The system consists of multiple microservices that process incoming build webhook requests, validate them, apply rate limiting, and dispatch them to a build runner.

Currently, the system is incomplete. You need to implement the request validation logic, configure the services to communicate with each other, and ensure the system is resilient against malicious or malformed payloads.

Here are the requirements:

1. **Implement the Payload Validator:**
   Write a Python module at `/home/user/app/gateway/validator.py` containing a function with the exact signature:
   `def validate_build_request(payload_str: str) -> bool:`
   
   This function must parse an incoming JSON string and return `True` if valid, or `False` if invalid.
   We have provided two directories containing test data:
   - `/home/user/app/corpora/clean/`: Contains valid build manifests (JSON).
   - `/home/user/app/corpora/evil/`: Contains malicious manifests (e.g., deeply nested JSON designed to cause memory issues, payloads with path traversal strings like `../` in the `build_target` field, and missing mandatory fields like `repository` or `commit_hash`).
   
   Your `validate_build_request` function must return `True` for 100% of the files in the `clean` corpus and `False` for 100% of the files in the `evil` corpus.

2. **Configure and Start the Services:**
   The build system relies on three services located in `/home/user/app/`:
   - **Redis:** Used for rate limiting. Start a local redis-server on the default port (6379).
   - **Build Dispatcher:** A mock Python service at `/home/user/app/dispatcher/app.py`. Start it on port 5001.
   - **Webhook Gateway:** A Flask app at `/home/user/app/gateway/app.py`. It requires `validator.py` to function. Start it on port 5000.
   
   You must modify `/home/user/app/gateway/config.ini` to properly link the Gateway to Redis (localhost:6379) and the Dispatcher (http://localhost:5001).

3. **Rate Limiting:**
   The Webhook Gateway has a rate-limiting middleware that you must enable by setting `RATE_LIMIT_ENABLED=true` in its config. It uses Redis to limit requests to 5 per minute per IP. 

Once you have written the validator and started all three services in the background, verify your setup by sending a few `curl` requests to `http://localhost:5000/webhook`. Write a summary log file to `/home/user/app/setup_complete.log` containing the text "SYSTEM_READY" when you are finished.