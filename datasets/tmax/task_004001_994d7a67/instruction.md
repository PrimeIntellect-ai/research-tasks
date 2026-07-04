You are a security researcher analyzing a suspicious, stripped binary found on a compromised server. The binary is located at `/app/bin/stat_analyzer`. It appears to be a data processing utility that accepts a stream of numeric data via standard input, performs some statistical aggregations, and outputs the results to standard output.

However, we've noticed that when processing certain data feeds, the binary stops producing output and consumes 100% CPU on multiple cores, indicating a deadlock or convergence failure within its multithreaded workers.

Your objective is to:
1. Use system call tracing tools (`strace`, `ltrace`, etc.) to analyze `/app/bin/stat_analyzer` and determine exactly what corrupted input bytes cause the threads to deadlock or fail to converge.
2. Build a robust Python HTTP wrapper service that safely exposes this binary. The service must run on `127.0.0.1:9000`.
3. The Python service should expose a `POST /process` endpoint. It must accept raw binary/text payloads, sanitize the corrupted input (removing or neutralizing the specific byte sequences that trigger the binary's bug), pass the cleaned data to the binary via a subprocess, and return the binary's standard output as the HTTP response.
4. If the service detects an unrecoverable payload that cannot be sanitized, it must return an HTTP 400 status code. 
5. The service must use an authentication token. It should only process requests containing the header `X-Auth-Token: SecRes2024`. Reject others with HTTP 401.
6. Create a regression test script at `/home/user/regression_test.sh` that uses `curl` to send both clean and intentionally corrupted payloads to your Python service, verifying that the deadlock is prevented and the correct HTTP status codes and outputs are returned. Write the output of these test runs to `/home/user/regression_results.log`.

Start the Python service in the background and leave it running. You are restricted to standard CLI tools and standard Python libraries (no external frameworks like Flask/FastAPI; use `http.server` or `socket`).