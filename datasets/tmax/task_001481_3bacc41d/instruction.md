As a release manager preparing for an infrastructure migration, you need to replace a legacy C-based evaluation service with a modern Python WebSocket architecture. The current service relies on an undocumented, stripped binary located at `/app/legacy_emu`. 

Your task is to reverse-engineer the simple stack-based language processed by the legacy binary, build a pure-Python emulator for it, and serve it via WebSockets with request validation and rate limiting.

Here are the requirements:

1. **Reverse-engineer the emulator:** 
   The binary at `/app/legacy_emu` takes a single file path as a command-line argument. The file contains a sequence of whitespace-separated tokens representing stack machine operations (including pushing integers, addition, subtraction, multiplication, and outputting the top of the stack). Figure out the instruction set by experimenting with the binary.

2. **WebSocket Server (`/home/user/server.py`):**
   - Must use `asyncio` and `websockets` to listen on `localhost:8765`.
   - Must accept incoming JSON messages with the schema: `{"client_id": "<string>", "code": "<string>"}`.
   - The `code` string contains the stack operations separated by spaces or newlines.
   
3. **Validation & Rate Limiting:**
   - Implement a rate limiter: A specific `client_id` may only make up to 5 requests per second.
   - If a client exceeds the limit, immediately reply with `{"error": "rate limited"}` and do not process the code.
   - If the JSON schema is invalid or missing fields, return `{"error": "invalid request"}`.

4. **Python Emulator Implementation:**
   - Write a Python interpreter for the reverse-engineered stack language within the server. 
   - **DO NOT** use `subprocess` to call the `/app/legacy_emu` binary in your server. You must implement the logic natively in Python.
   - If the code executes successfully, return `{"result": "<emulated_output>"}`. The `<emulated_output>` should exactly match what the legacy binary would print to stdout.
   - If a stack underflow occurs during emulation, the binary prints a specific error word. Your Python emulator must replicate this error behavior and return it in the result string.

5. **End-to-End Test Orchestration (`/home/user/e2e_test.py`):**
   - Write a Python script that programmatically starts `/home/user/server.py` as a background process.
   - Connects to the WebSocket server as a client.
   - Sends a payload that calculates `(10 + 5) * 2` and outputs the result, verifying the response.
   - Tests the rate-limiting functionality by intentionally spamming requests from the same `client_id` and asserting that the rate limit error is returned.
   - Automatically kills the server process and cleans up before exiting.
   - Prints "ALL TESTS PASSED" if everything works.

Your solution will be evaluated programmatically. An external verifier will send thousands of randomly generated valid and invalid bytecode sequences to your WebSocket server and compare the outputs (and rate-limiting behavior) against the gold standard.