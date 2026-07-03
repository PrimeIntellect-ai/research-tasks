You are a Site Reliability Engineer tasked with monitoring the uptime and availability of several new local endpoints. Your goal is to set up a secure local web server, extract the list of endpoints from a messy log file, and write a C health-checker program to verify their status.

Perform the following steps exactly as specified. All work must be done within `/home/user`.

1. **Web Server Setup & TLS Configuration**:
   - Create a directory called `/home/user/www`.
   - Inside `/home/user/www`, create two files: `healthz` (containing the word "OK") and `metrics` (containing the word "prometheus").
   - Generate a self-signed SSL certificate (`cert.pem`) and an unencrypted private key (`key.pem`) in `/home/user`. Use `localhost` as the Common Name (CN).
   - Start a local HTTPS web server on `127.0.0.1` port `8443` serving the `/home/user/www` directory using the generated certificate and key. Ensure this process runs in the background.

2. **Text Processing**:
   - You have been provided a file at `/home/user/raw_endpoints.txt`.
   - Use text processing tools (`awk`, `sed`, `grep`, etc.) to extract just the URI paths (the strings beginning with `/`) from each line. 
   - Save the cleaned, extracted paths into `/home/user/clean_paths.txt` (one path per line).

3. **C Health Checker**:
   - Write a C program at `/home/user/checker.c` that reads `/home/user/clean_paths.txt`.
   - For each path, the C program must use `libcurl` to make an HTTPS GET request to `https://127.0.0.1:8443<path>`.
   - Since you are using a self-signed certificate, ensure your `libcurl` configuration disables SSL peer and host verification.
   - The program must capture the HTTP response status code for each path.
   - The program must output the results directly to `/home/user/status_report.csv` in the exact format: `path,http_status_code` (e.g., `/healthz,200`).
   - Compile your program into an executable named `/home/user/checker` and run it.

Ensure the final `status_report.csv` file is perfectly formatted.