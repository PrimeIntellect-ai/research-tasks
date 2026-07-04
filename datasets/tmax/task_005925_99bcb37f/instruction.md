You are an integration developer modernizing an old API system. You need to implement an API gateway (reverse proxy) that routes traffic between a legacy backend and a new emulated backend based on Semantic Versioning, and then verify the system. 

Here are the requirements:

1. **Legacy Backend (V1)**: 
   There is a script located at `/home/user/backend_v1.py` (which has already been created for you). It runs an HTTP server on port 8001. You will need to start it in the background. It responds to all POST requests with the string: `V1 Legacy API`.

2. **New Emulated Backend (V2)**:
   Create a Python script at `/home/user/backend_v2.py` that runs an HTTP server on port 8002. This backend must act as an interpreter for a custom string-manipulation command language. It should accept HTTP POST requests with a raw text body. The body will contain a single command followed by a space and an argument string. 
   Supported commands:
   - `ECHO <string>`: Returns the exact `<string>`.
   - `REVERSE <string>`: Returns the `<string>` reversed.
   - `UPPER <string>`: Returns the `<string>` in all uppercase.
   If the command is unknown or missing, it should return exactly `ERROR`.

3. **Semantic Versioning Reverse Proxy**:
   Create a Python script at `/home/user/proxy.py` that runs an HTTP server on port 8000. This proxy must examine incoming POST requests for an HTTP header named `X-API-Version`. 
   - You must parse the version header as a Semantic Version (MAJOR.MINOR.PATCH).
   - If the version is `>= 2.0.0` (e.g., `2.0.0`, `2.1.5`, `10.0.0`), forward the exact request (headers and body) to the V2 backend on port 8002, and return its response to the client.
   - If the version is `< 2.0.0` (e.g., `1.9.9`, `1.12.0`, `0.5.0`), or if the header is missing entirely, forward the request to the V1 backend on port 8001, and return its response.
   - *Note: Be careful with semantic version logic (e.g., `1.12.0` is greater than `1.9.0`).*

4. **Verification Log**:
   Start all three servers in the background. Then, execute the following specific `curl` commands and append their raw output (just the response body, no newlines between outputs unless the server provides them) into a single file at `/home/user/results.log`. 

   Run these exactly in this order:
   1. `curl -s -X POST -H "X-API-Version: 1.9.5" -d "REVERSE hello" http://localhost:8000/`
   2. `curl -s -X POST -H "X-API-Version: 1.12.0" -d "REVERSE hello" http://localhost:8000/`
   3. `curl -s -X POST -H "X-API-Version: 2.0.0" -d "REVERSE hello" http://localhost:8000/`
   4. `curl -s -X POST -H "X-API-Version: 2.10.1" -d "UPPER world" http://localhost:8000/`
   5. `curl -s -X POST -d "ECHO missing_header" http://localhost:8000/`

Ensure that the servers are running correctly and the log file `/home/user/results.log` is generated with the exact responses stringed together or line-by-line depending on how `curl` outputs it. Do not add any extra text to the log file.