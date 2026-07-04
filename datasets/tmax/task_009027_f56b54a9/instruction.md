You are an integration developer tasked with building a lightweight, custom API testing framework. Standard testing tools are unavailable in this environment, so you must build a C-based rule evaluator, a mock API server, and an orchestration script to run end-to-end tests.

Your objective is to complete the following components in `/home/user`:

1. **The Rule Evaluator (`/home/user/api_evaluator.c`)**:
   Write a C program that acts as a mini-interpreter for our custom API testing DSL. 
   - It must take exactly two command-line arguments: a state string and a rule string.
   - The state string format will always be: `STATUS=<int>,TIME=<int>` (e.g., `STATUS=200,TIME=45`). TIME represents milliseconds.
   - The rule string format evaluates one or two conditions. It follows the pattern: `VAR OP VAL [AND VAR OP VAL]`
     - `VAR` can be `STATUS` or `TIME`.
     - `OP` can be `==`, `<`, or `>`.
     - `VAL` is an integer.
     - Optional conjunction `AND` (there will be at most one `AND` in a rule).
     - Example rules: `"STATUS == 200"`, `"STATUS == 200 AND TIME < 100"`.
   - The program must parse the state string, evaluate the rule string against the state, and print exactly `PASS` or `FAIL` to standard output (with a newline), then exit with code 0.

2. **The Mock API Server (`/home/user/mock_server.py`)**:
   Create a Python 3 HTTP server (using `http.server` or similar built-in libraries, do not use external libraries like Flask) that listens on `127.0.0.1:8080`. It must implement three endpoints:
   - `GET /success` : Waits for 10ms, then returns a 200 OK status.
   - `GET /timeout` : Waits for 150ms, then returns a 200 OK status.
   - `GET /error`   : Waits for 10ms, then returns a 500 Internal Server Error status.

3. **The E2E Test Runner (`/home/user/test_runner.sh`)**:
   Write a bash script that tests the mock server using `curl` and your C evaluator.
   - The script must loop through the three endpoints (`/success`, `/timeout`, `/error`).
   - For each endpoint, use `curl` to fetch the endpoint on `http://127.0.0.1:8080`. Extract the HTTP status code and the total time taken in milliseconds.
   - Construct the state string: `STATUS=<status>,TIME=<time_ms>`.
   - Run the `./api_evaluator` binary with the state string and the following expected rules:
     - For `/success`: `"STATUS == 200 AND TIME < 100"`
     - For `/timeout`: `"STATUS == 200 AND TIME > 100"`
     - For `/error`: `"STATUS == 500 AND TIME < 100"`
   - Append the output of the evaluator to `/home/user/test_report.txt` in the exact format: `[endpoint] -> [PASS/FAIL]` (e.g., `/success -> PASS`).

4. **The CI/CD Pipeline (`/home/user/Makefile`)**:
   Write a `Makefile` with a `test` target that acts as a local CI pipeline step. Running `make test` must:
   1. Compile `api_evaluator.c` into an executable named `api_evaluator`.
   2. Start `mock_server.py` in the background.
   3. Wait briefly (e.g., 1-2 seconds) to ensure the server is listening.
   4. Execute `test_runner.sh`.
   5. Safely terminate the background `mock_server.py` process.

Ensure all scripts have execute permissions where necessary. Do not include any hardcoded test results in your report; it must be generated dynamically.