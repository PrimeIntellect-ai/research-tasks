You are an integration developer tasked with securing our internal API gateway. We have a legacy routing engine provided as a compiled binary at `/app/legacy_router`. This binary parses API request parameters and routes them to backend services. However, a recent security audit revealed that it is vulnerable to parameter pollution and constraint violation attacks when handling complex nested JSON data embedded in the URL parameters.

Your objective is to write a Python-based pre-filter script at `/home/user/api_filter.py` that sanitizes and validates incoming requests before they reach the legacy router. 

To succeed, you must:
1. Analyze the `/app/legacy_router` binary (it is stripped, so you may need to run strings, strace, or treat it as a black box). It takes a single argument: the full API path including query parameters (e.g., `/api/v1/resource?config={"key":"value"}`). Determine the implicit constraints it enforces on routing parameters (like length limits, disallowed characters, and nested depth).
2. Implement `/home/user/api_filter.py`. This script must:
   - Accept a single command-line argument: a file path containing a list of API URLs (one per line).
   - Parse the URL routing parameters and extract the embedded structured data (JSON strings inside query parameters).
   - Evaluate the extracted data against the constraints you discovered from the binary.
   - For each URL in the file, print exactly one line to standard output: `ACCEPT: <url>` if it is safe, or `REJECT: <url>` if it violates the constraints or contains malicious payloads designed to exploit the router.

We have provided two directories of test cases for you to validate against:
- `/app/corpus/clean/`: Contains text files with valid, well-formed API requests that your filter MUST accept.
- `/app/corpus/evil/`: Contains text files with malicious or malformed requests (e.g., bypassing routing bounds, parameter injection) that your filter MUST reject.

Ensure your Python script is executable and uses standard libraries only (e.g., `urllib`, `json`).