We are porting an old mathematical CLI tool to run as a microservice in a minimal container. You need to build a Python web service, implement secure mathematical parsing, add rate limiting, and set up a basic CI test script. 

Please perform the following tasks in the `/home/user/math_service` directory (create it if it doesn't exist):

1. **Web Service (`server.py`)**:
   Create a Flask web application running on `127.0.0.1:8080`. 
   - It must have a single endpoint: `POST /evaluate`.
   - The endpoint accepts JSON with the format: `{"payload": "<base64_encoded_expression>"}`.
   - **Data Encoding & Validation**: Decode the base64 payload. Before evaluating, you MUST validate that the decoded string contains ONLY the following characters: numbers (`0-9`), operators (`+`, `-`, `*`, `/`), parentheses (`(`, `)`), periods (`.`), and spaces. If any other character is present (or if base64 decoding fails), return an HTTP `400 Bad Request` with `{"error": "Invalid input"}`.
   - **Expression Evaluation**: If valid, mathematically evaluate the string and return HTTP `200 OK` with `{"result": <numeric_result>}`.
   - **Rate Limiting**: Implement an in-memory rate limiter. A single IP can only make 5 requests to `/evaluate` per 60-second rolling window. The 6th request within 60 seconds must return HTTP `429 Too Many Requests` with `{"error": "Rate limit exceeded"}`.

2. **Test Fixtures & Mocks (`test_server.py`)**:
   Write a `pytest` suite for the application.
   - Test valid evaluation.
   - Test invalid character rejection (the 400 error).
   - Test the rate limiter (the 429 error). You must use the `unittest.mock.patch` module to mock the time module (e.g., `time.time`) so that your rate limit test executes instantly without actually sleeping for 60 seconds.

3. **CI/CD Script (`ci_run.sh`)**:
   Create a bash script at `/home/user/math_service/ci_run.sh` that sets up any necessary Python environment, installs `flask` and `pytest`, and runs the `test_server.py` suite. The script must exit with `0` if tests pass, and `1` if they fail. Make the script executable.

Ensure your code handles division by zero gracefully (return `400 Bad Request`). You can use the built-in `eval` ONLY because you strictly validate the character set beforehand.