You have inherited an unfamiliar, buggy multi-service application located in `/app/src`. The system is designed to process high-value financial transactions, but it is currently failing in production. 

The application consists of three cooperating Python services:
1. **Database Service** (`/app/src/db.py`): A simple TCP key-value store listening on port 7070.
2. **Worker Service** (`/app/src/worker.py`): A backend processing engine listening for TCP connections on port 9090.
3. **API Gateway** (`/app/src/gateway.py`): An HTTP server listening on port 8080. It accepts POST requests, serializes the data, and forwards it to the worker.

**The Problem:**
When testing on local 32-bit and 64-bit x86 environments with small transaction IDs, everything works. However, in staging, when the API Gateway receives production-sized transaction payloads (which contain large 64-bit integer IDs like `9007199254740991`), the application fails. The worker process crashes, producing a stack trace in `/tmp/worker.log` and dropping the connection.

**Your Objectives:**
1. **Diagnose:** Start the services and send test requests to reproduce the crash. Analyze the stack trace and data flow to locate the bug. You will find that precision loss and an integer overflow during network serialization (`struct.pack/unpack`) between the gateway and the worker are causing the IDs to be corrupted.
2. **Fix:** Correct the serialization protocol in both `gateway.py` and `worker.py` so that large 64-bit integers are transmitted exactly without precision loss.
3. **Validate:** Add strict assertion-based intermediate validation in `worker.py` right after deserialization to ensure `type(transaction_id) is int` and that it matches expected bit-bounds, preventing silent corruption in the future.
4. **Deploy:** Start all three services in the background. The API Gateway MUST listen on `127.0.0.1:8080`. 

**Final State Verification:**
Leave all three services running. An automated verifier will send HTTP POST requests to `http://127.0.0.1:8080/process` with a JSON body like `{"tx_id": 9007199254740993, "amount": 250.50}`. It expects an HTTP 200 response with JSON `{"status": "success", "processed_id": 9007199254740993}`.