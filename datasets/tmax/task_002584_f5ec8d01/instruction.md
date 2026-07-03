You are an integration developer building the backend for a web security gateway. We use a high-speed, sandboxed C-based interpreter called `miniscript` to evaluate custom security rules against incoming web requests. 

Your task is to fix the provided `miniscript` package, benchmark it, and wrap it in a multi-protocol Python service.

**Step 1: Fix and Compile the Interpreter**
The source code for `miniscript` is vendored at `/app/vendor/miniscript`. 
Unfortunately, the `Makefile` is broken. It fails to compile due to a typo in the compiler flags and a missing math library linkage.
1. Fix the `/app/vendor/miniscript/Makefile`.
2. Run `make` to build the shared library `libminiscript.so`.

**Step 2: Performance Benchmarking**
We need to ensure the C-engine is fast enough. Write a Python script at `/app/benchmark.py` that uses the `ctypes` module to load `libminiscript.so`. 
The library exports a function: `int evaluate_rule(const char* script, const char* input_data);`.
Write a script that calls `evaluate_rule("return input == 'malicious';", "malicious")` 100,000 times. Record the total elapsed time in seconds as a single float value in `/app/bench_result.txt`.

**Step 3: Implement the Integration API Service**
Create and start a Python service at `/app/server.py` that exposes the `miniscript` engine over two protocols concurrently.

**Protocol A: HTTP REST**
- Listen on `127.0.0.1:8080`.
- Endpoint: `POST /api/v1/evaluate`
- Security: Require the header `Authorization: Bearer sec-token-999`. Return `401 Unauthorized` if missing or incorrect.
- Request Body (JSON): `{"rule": "<script code>", "payload": "<input data>"}`
- Response (JSON): `{"result": <integer returned by evaluate_rule>}`

**Protocol B: Raw TCP**
- Listen on `127.0.0.1:8081`.
- Wait for incoming connections. For each line received (terminated by `\n`), parse it as `RULE|PAYLOAD`.
- Evaluate the rule and payload, and send back the integer result as a string followed by `\n`.
- This is a fast-path internal protocol without auth.

Start your server in the background so it is running when your task finishes. Both ports must be actively listening. Use standard libraries (e.g., `http.server`, `socketserver`, `threading`, or `Flask`/`FastAPI` if you install them, though standard library is sufficient).