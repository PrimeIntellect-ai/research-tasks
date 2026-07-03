You are a performance and debugging engineer investigating a broken multi-service application located in `/app`. The application consists of a Python-based HTTP frontend and a C-based TCP backend that performs data transformation (a custom text encoding).

Currently, the system is completely non-functional:
1. The C backend fails to build due to linker errors.
2. Even when built, the backend produces incorrect output during data transformation.

Your objectives:
1. Diagnose and fix the build failures in `/app/backend`. You are allowed to modify the `Makefile` and C source files as needed to resolve undefined references.
2. Once built, use the provided `/app/start.sh` to bring up both the frontend (listening on `127.0.0.1:8080`) and the backend (listening on `127.0.0.1:9090`).
3. Investigate the data transformation logic in the C backend. We have provided `/app/sample_in.txt` and `/app/sample_out_expected.txt`. The HTTP API endpoint `http://127.0.0.1:8080/transform` accepts POST requests with raw text and returns the transformed text. Use standard diff tools to analyze the transformation discrepancies and fix the bug in the C code so the output perfectly matches the expected text.
4. Write a regression test script at `/home/user/test.sh` (make it executable) that sends the contents of `/app/sample_in.txt` to the frontend via `curl` (POST to `http://127.0.0.1:8080/transform`) and strictly compares the HTTP response body against `/app/sample_out_expected.txt`. The script must exit with `0` if they match, and `1` otherwise.

Ensure that by the end of your task, both services are running continuously in the background so that external clients can verify the HTTP API.