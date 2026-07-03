You are a web developer building a new Text Processing feature. Our core text processing logic has been implemented as a gRPC service, but our frontend requires a RESTful HTTP JSON API. 

Your task is to:
1. Compile the provided protocol buffer file into Python stubs.
2. Build a Python-based HTTP reverse proxy that routes REST requests to the gRPC backend.
3. Orchestrate an End-to-End (E2E) test script to verify the full flow.

**Setup & Environment:**
The working directory is `/home/user/app`. Inside, you will find:
* `requirements.txt`: Contains `grpcio`, `grpcio-tools`, `Flask`, and `requests`. Install these dependencies first.
* `processor.proto`: The gRPC service definition.
* `backend.py`: A fully implemented gRPC server listening on `localhost:50051`.

**Step 1: Protocol Buffers**
Compile `processor.proto` into Python stubs in the `/home/user/app` directory. 

**Step 2: HTTP Reverse Proxy**
Create `/home/user/app/proxy.py` using Flask. The proxy must:
* Listen on `0.0.0.0` port `8080`.
* Implement a route: `GET /api/v1/process/<action>`
* Accept a query parameter `text` (e.g., `?text=hello`).
* The `<action>` URL parameter will be either the string `upper` or `reverse`.
* Parse these parameters, map the `action` string to the corresponding gRPC `Action` enum (defined in the proto), and make an RPC call to `ProcessText` on `localhost:50051`.
* Return the gRPC response as a JSON object: `{"result": "<processed_string>"}`. If the action is invalid, return HTTP 400.

**Step 3: End-to-End Test Orchestration**
Create a bash script `/home/user/app/run_e2e.sh` that:
1. Starts `backend.py` in the background.
2. Starts `proxy.py` in the background.
3. Waits for both services to become available (e.g., using `sleep` or polling).
4. Uses `curl` to send two test requests:
   - Action: `upper`, Text: `hello e2e`
   - Action: `reverse`, Text: `protobuf`
5. Verifies the expected JSON responses. If both responses are exactly correct (`{"result": "HELLO E2E"}` and `{"result": "fubotorp"}`), write the exact string `E2E_ALL_PASS` to `/home/user/app/test_results.log`. Otherwise, write `E2E_FAIL`.
6. Gracefully kills both background processes before exiting.

Ensure your script is executable (`chmod +x run_e2e.sh`). We will verify your task by running your E2E script and checking the log, as well as manually testing your proxy.