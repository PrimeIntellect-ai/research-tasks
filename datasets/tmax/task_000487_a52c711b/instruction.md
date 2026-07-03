We are investigating a suspected breach in our internal logging infrastructure. The attackers deployed an obfuscated binary (`/app/bin/obfuscated_logger`) that intercepts log messages, appends a cryptographic hash, and forwards them to our internal multi-tier logging service. We need to completely understand what this binary is doing and restore our services using a clean, auditable implementation.

First, you need to write a clean Python script (`/home/user/clean_logger.py`) that exactly reproduces the output of the `/app/bin/obfuscated_logger` binary. The binary takes a single command-line argument (a log string) and outputs a transformed string containing the original message and a generated checksum/signature. You must analyze the binary's behavior (it uses standard cryptographic hashing) and write a Python script that takes a single command-line argument and prints the exact same output string as the binary for any given input.

Second, our logging infrastructure is currently offline due to configuration tampering. The infrastructure consists of three services located in `/app/services/`:
1.  An Nginx reverse proxy (listening on port 8080)
2.  A Redis queue (listening on port 6379)
3.  A Python backend worker (`/app/services/backend/worker.py`)

The end-to-end flow should be: HTTP POST requests with a raw body (the output of your `clean_logger.py`) sent to `http://localhost:8080/log` must be accepted by Nginx, routed to a local Lua script that pushes the raw body to the Redis list `incoming_logs`, and then the Python backend worker must pop from this list and write the verified logs to `/home/user/verified_logs.txt`.
Currently, the Nginx configuration (`/app/services/nginx/nginx.conf`) is broken, the Redis connection strings in the backend worker are wrong, and the services are not communicating. 

Your tasks:
1. Create `/home/user/clean_logger.py` that is bit-exact equivalent in its standard output to `/app/bin/obfuscated_logger` for any string input.
2. Fix the configurations in `/app/services/nginx/nginx.conf` and `/app/services/backend/worker.py`.
3. Start the Redis server, the Python backend worker, and Nginx.
4. Verify the end-to-end flow works by sending a test log through your Python script and then via `curl` to the Nginx endpoint.