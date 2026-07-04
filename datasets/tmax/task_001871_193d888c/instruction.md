You are a security researcher analyzing a new strain of multithreaded malware that uses a custom mathematical obfuscation scheme. 

We have recovered a partially complete Python package, `obfuscation_solver`, located at `/app/obfuscation_solver`. It is supposed to reverse the obfuscation, but it currently has several critical bugs:
1. **Numerical Instability:** The core mathematical decoding routine in `obfuscation_solver/math_utils.py` suffers from catastrophic cancellation when calculating the activation function for large negative inputs, resulting in wild inaccuracies.
2. **Encoding/Serialization Issues:** The malware sends 64-bit integer keys in its binary payload, but `obfuscation_solver/serializer.py` incorrectly unpacks them, leading to truncated results.
3. **Concurrency Deadlock:** The solver uses a custom thread pool in `obfuscation_solver/decoder.py` to process blocks in parallel. Under high contention, threads frequently deadlock. You will need to use delta debugging and assertion-based validation to isolate why the locks are not being released properly.

Your task:
1. Debug and fix the `/app/obfuscation_solver` package so that it correctly and reliably decodes payloads without hanging or returning mathematically incorrect/truncated keys.
2. Create an HTTP service using Python (e.g., Flask, FastAPI, or standard library) that acts as an analysis oracle for other researchers.
3. The server MUST listen on `127.0.0.1:9090`.
4. It must expose a `POST /decode` endpoint.
5. The endpoint MUST require authentication via an HTTP header: `Authorization: Bearer sec-research-agent-2024`. Reject requests without this exact header with a 401 Unauthorized status.
6. The endpoint will receive a JSON payload like: `{"payload": "<base64_encoded_binary_string>"}`.
7. You must base64-decode the string, pass the bytes to the fixed `obfuscation_solver.decoder.decode_payload(data)` function, and return a JSON response in the exact format: `{"decoded_key": 123456789012345, "status": "success"}`.
8. Start the server in the background and ensure it is running and ready to accept requests.

Create a log file at `/tmp/server_ready.log` containing the text "READY" once your server is listening and the package is fixed.