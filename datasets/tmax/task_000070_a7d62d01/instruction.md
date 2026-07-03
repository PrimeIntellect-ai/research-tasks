A contributor has submitted a Pull Request to our open-source data processing project, but the PR is currently failing CI and the original author is unresponsive. 

The PR introduces a highly optimized, pre-compiled shared library (`libfastxor.so`) because the contributor claims it significantly speeds up our data masking routines. Unfortunately, they only provided the stripped binary and a broken Python integration. 

You need to step in as the maintainer, review the broken PR, and get the system ready for production.

The PR files are located at `/app/pr_workspace/`. You will find:
1. `/app/pr_workspace/libfastxor.so`: The stripped, compiled shared library.
2. `/app/pr_workspace/wrapper.py`: A Python file using `ctypes` to interface with the library. It is currently crashing (segmentation faults) or returning garbage data.
3. `/app/pr_workspace/test_wrapper.py`: A test suite using the `hypothesis` library (property-based testing). It consistently fails.
4. `/app/pr_workspace/server.py`: A skeleton for an HTTP API that should expose the library's functionality.

Your tasks:
1. **Fix the ABI Binding**: Reverse-engineer or debug the interaction with `/app/pr_workspace/libfastxor.so` to figure out the correct function signatures and memory management in `wrapper.py`. The library exports a dynamic symbol `mask_payload`.
2. **Pass the Tests**: Modify `wrapper.py` until `pytest /app/pr_workspace/test_wrapper.py` passes 100% of its property-based tests. You will likely need to manage dependencies (e.g., installing `pytest` and `hypothesis`).
3. **Build the API**: Implement the FastAPI application in `/app/pr_workspace/server.py`. It must expose a `POST` endpoint at `/mask` that accepts a JSON payload: `{"payload": "<base64_encoded_string>", "key": <integer>}`. It should decode the base64 payload, process it using the fixed `wrapper.py`, and return JSON: `{"masked_base64": "<base64_encoded_string>"}`.
4. **Deploy**: Start the API server on `127.0.0.1:8080` in the background and leave it running. Write a log file to `/app/pr_workspace/server.log` capturing the server's stdout/stderr.

Do not modify the test file (`test_wrapper.py`) or the shared library (`libfastxor.so`). You may only modify `wrapper.py` and `server.py`, and install necessary Python packages.