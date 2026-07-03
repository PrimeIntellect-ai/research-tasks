You are a systems programmer working on a new Python REST API that evaluates mathematical expressions. For performance and legacy reasons, the core expression parser is written in C (`math_eval.c`) and compiled into a shared library (`libmatheval.so`). 

However, the current Python integration is broken due to library linking issues and incorrect data encoding.

Your task:
1. Navigate to `/home/user/api/`.
2. The Makefile successfully builds `libmatheval.so`, but `main.py` crashes on startup because it cannot locate or correctly bind to the shared library. Fix the `ctypes` library loading in `main.py` so the FastAPI app starts successfully.
3. The C function `evaluate_hex_expr` expects the input expression to be passed as a **hex-encoded string** (e.g., the expression `1+2` must be passed to the C function as the string `"312b32"`). Currently, `main.py` incorrectly passes raw UTF-8 bytes. Fix the endpoint `/evaluate` in `main.py` to properly encode the incoming expression into a hex string before passing it to the C library.
4. Create a property-based test file at `/home/user/api/test_api.py` using `pytest` and `hypothesis`. Write a test that generates random addition expressions (e.g., strings of random integers separated by `+`, like `15+2+99`) and sends them to the `/evaluate` endpoint via `fastapi.testclient.TestClient`. The test must assert that the response status code is 200.
5. Run your test and save the output to `/home/user/api/test_results.log`.

Ensure all dependencies are met. You can install missing standard python packages if needed (`fastapi`, `uvicorn`, `pytest`, `hypothesis`, `requests`, `httpx`).