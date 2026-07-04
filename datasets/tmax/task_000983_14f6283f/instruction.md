We are building a new polyglot log ingestion pipeline. The system consists of a high-performance Rust TCP service for parsing log events using a custom state machine, a Python HTTP API gateway for request validation and rate limiting, and a Redis instance for tracking rate limits.

The initial scaffolding has been created in `/home/user/log-pipeline`, but the previous engineer left it in a broken state. Your task is to fix the compilation issues, implement the missing gateway logic, and create a build/startup script that brings everything up.

Here is the current state of `/home/user/log-pipeline`:
1. `rust-parser/`: Contains a Rust TCP server that accepts raw log strings, parses them using a state machine, and returns JSON. It currently fails to compile due to ownership and borrow checker errors.
2. `python-gateway/`: Contains a skeleton Python script `gateway.py` that needs to be implemented.
3. `redis/`: Redis is installed on the system, but you need to ensure it's running.

Your objectives:
1. **Fix the Rust Service**: Modify `/home/user/log-pipeline/rust-parser/src/main.rs` to fix the borrow checker errors in the log parsing state machine. Do not change the logic or the parsing rules; just fix the ownership issues so it compiles and runs. It must listen on `127.0.0.1:9090`.
2. **Implement the Python Gateway**: Write the logic in `/home/user/log-pipeline/python-gateway/gateway.py` (you may use Flask, FastAPI, or standard library). 
   - It must listen for HTTP POST requests on `127.0.0.1:8080` at the endpoint `/ingest`.
   - It must require an `Authorization` header with the exact format `Bearer <token>`. 
   - It must enforce a rate limit of exactly 5 requests per second per token using Redis (running on `127.0.0.1:6379`). Exceeding this should return HTTP 429.
   - Valid, rate-limited requests should extract the plaintext body, forward it over a TCP socket to the Rust service on `127.0.0.1:9090`, read the JSON response, and return it to the client with HTTP 200.
3. **Build & Orchestrate**: Create a bash script at `/home/user/log-pipeline/start_all.sh` that compiles the Rust binary (in release mode), starts Redis locally, runs the Rust TCP service in the background, and runs the Python HTTP gateway in the background. The script should exit 0 and leave the services running.

Make sure the services stay running after your script finishes. Create an application log file at `/home/user/log-pipeline/app.log` and redirect all stdout/stderr from the Python and Rust services there so we can verify they started correctly.