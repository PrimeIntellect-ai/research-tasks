You are an engineer porting a backend service's rate limiting and request validation logic to a minimal container environment. To reduce dependencies, the new tool must be implemented as a standalone Bash/shell script (using only standard tools like `awk`, `grep`, `bash`, `coreutils`), but you will use Python to create the test fixtures and verify its behavior.

Your objective:
1. Create a shell script at `/home/user/rate_limit.sh` that reads log entries from `stdin` and processes them.
2. Create a Python test suite at `/home/user/test_limiter.py` that tests your script using mock data.

**Requirements for `/home/user/rate_limit.sh`:**
- Reads lines from standard input in the format: `<unix_timestamp> <ip_address> <request_path>` (space-separated).
- **Validation**: The `<request_path>` must begin exactly with `/api/`. If it does not, the script must output: `INVALID <ip_address> <request_path>`.
- **Rate Limiting**: For valid `/api/` requests, apply a fixed-window rate limit of **maximum 2 requests per IP per second**.
  - If the request is within the limit, output: `ALLOW <ip_address> <request_path>`.
  - If the limit is exceeded for that IP in that exact second, output: `DENY <ip_address> <request_path>`.
- The script must process the lines in the order they are received.
- Make sure the script is executable (`chmod +x`).

**Requirements for `/home/user/test_limiter.py`:**
- Must be a Python script that executes `/home/user/rate_limit.sh` via `subprocess`.
- Must generate mock test data that covers:
  - Valid paths that are allowed (<= 2 requests/sec).
  - Valid paths that are denied (> 2 requests/sec).
  - Invalid paths (e.g., `/home`, `/API/`, `api/test`).
- Must assert the output of the shell script matches the expected behavior.
- Must exit with code `0` on success, and non-zero if tests fail.

Ensure both files are created with the correct logic. The automated grading system will run your Python test script, and will also test your shell script against a hidden set of log entries to verify its correctness.