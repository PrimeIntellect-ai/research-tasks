We are migrating a small data processing microservice to a highly minimal container environment that lacks a Python interpreter. Currently, our data extraction tool is written in Python, but we need it translated into a pure Bash script that relies only on standard Linux coreutils (like `grep`, `sed`, `awk`, `base64`, `tr`). 

Your task involves three steps:

**Step 1: Code Translation**
I have placed the legacy Python script at `/home/user/api_parser.py`. It parses a URL, extracts specific query parameters (`id` and `payload`), decodes the base64-encoded `payload`, and outputs a formatted string. 
Read this script and translate its exact functionality into a Bash script located at `/home/user/api_parser.sh`. The bash script must take the URL as its first positional argument (`$1`). Make sure `/home/user/api_parser.sh` is executable.

**Step 2: URL Parsing & Data Encoding Handling in Bash**
Ensure your Bash script properly extracts the `id` and `payload` parameters from the query string, regardless of the order they appear in the URL. If a parameter is missing, its value should be treated as an empty string. The `payload` value must be base64-decoded. 
The output format must identically match the Python script's output: `{"id": "ID_VALUE", "data": "DECODED_PAYLOAD"}`.

**Step 3: End-to-End Test Orchestration**
To verify your translated script works correctly, create an end-to-end test runner script at `/home/user/test_runner.sh`. This script must call your `/home/user/api_parser.sh` exactly three times in the following order, using these specific URLs:
1. `http://example.com/api?id=99&payload=QmFzaCBpcyBmdW4=`
2. `http://test.local/run?payload=T25seSBQYXlsb2Fk&id=42`
3. `http://app.net/v1?id=7`

The `test_runner.sh` script must redirect the standard output of these three calls, in order, into a single log file at `/home/user/test_results.log`.

Make sure you execute `/home/user/test_runner.sh` so that `/home/user/test_results.log` is generated before you complete the task.