You are acting as a log analyst investigating suspicious error patterns in a web server environment. You need to fix a broken vendored log processing tool, process a large dataset of raw logs, and expose your findings via a lightweight HTTP server written purely in Bash.

**Part 1: Fix the Vendored Package**
You have been provided with a vendored package at `/app/bash-log-utils` (version 1.0.0). This package contains a utility to stratify HTTP errors from TSV logs. However, the package is broken due to a deliberate perturbation:
1. The `bin/stratify_errors.sh` script has a bug where it prematurely exits after processing a few lines, preventing large-scale sampling.
2. Fix the script so it correctly processes the entire input stream, taking exactly 2 samples per endpoint that has an HTTP status >= 400.
3. Fix the `Makefile` if necessary and run `make install` to install the tool to `/home/user/bin/stratify_errors`.

**Part 2: Multi-Stage Data Pipeline**
A raw log file is located at `/home/user/raw_logs.tsv`. Its format is tab-separated:
`TIMESTAMP \t IP \t METHOD \t ENDPOINT \t STATUS \t BYTES`

Using Bash, coreutils, and your newly fixed `stratify_errors` tool:
1. Find the top 5 endpoints that returned error status codes (>= 400). Sort them by frequency (descending). Save this exact list (just the endpoint paths, one per line) to `/home/user/top_errors.txt`.
2. Use the `stratify_errors` tool to extract a stratified sample of the error logs (2 logs per error endpoint). Save this output to `/home/user/stratified_errors.tsv`.

**Part 3: Multi-Protocol Data Exposure**
Write a Bash script at `/home/user/server.sh` and run it in the background. It must implement a simple HTTP server using `nc` (netcat) or Bash's `/dev/tcp` listening on `127.0.0.1:9090`.
The server must continuously listen and handle these HTTP GET requests:
- `GET /health` -> Must return a valid HTTP 200 OK response with the body `OK`.
- `GET /top-errors` -> Must return a valid HTTP 200 OK response with the body being a JSON array of the top 5 error endpoints you found in Part 2. Example: `["/api/login", "/admin", "/wp-login.php", "/search", "/checkout"]`.

Ensure your server runs continuously and can handle multiple sequential requests. Do not use external web servers like Python's `http.server` or Nginx; stick entirely to Bash and `nc`.