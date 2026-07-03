You are an observability engineer tasked with setting up a secure local metrics dashboard backend and automating its deployment. You need to parse messy historical logs, expose the aggregated data via a secure Python web server, and create an idempotent script to manage the server's lifecycle.

Perform the following tasks in the `/home/user` directory:

1. **Log Processing Pipeline**:
   You have a raw log file at `/home/user/raw_logs.txt`. It contains mixed log entries.
   Extract only the lines containing the tag `[METRIC]`. Each of these lines has the format:
   `TIMESTAMP [METRIC] service=<service_name> response_time=<integer_ms>`
   Calculate the average `response_time` for each unique `service_name`.
   Save the result as a strictly formatted JSON file at `/home/user/parsed_metrics.json`. The keys must be the service names and the values must be the integer averages (rounded down to the nearest whole number). Example format:
   `{"auth-service": 145, "billing-service": 210}`

2. **TLS Configuration & Web Server**:
   Create a directory `/home/user/certs`. Generate a self-signed RSA-2048 certificate (`cert.pem`) and private key (`key.pem`) valid for 365 days in this directory. Do not encrypt the private key.
   Write a Python script at `/home/user/secure_api.py` that implements a basic HTTPS server listening on `localhost` port `9443`.
   When a `GET` request is made to the `/metrics` path, the server must read `/home/user/parsed_metrics.json` and serve its contents with a `200 OK` status and `Content-Type: application/json`. Any other path should return `404 Not Found`.
   The server must use the generated `cert.pem` and `key.pem` for TLS.

3. **Idempotent Deployment Script**:
   Write a script at `/home/user/manage_services.sh`. When executed, this script must:
   - Check if `secure_api.py` is currently running.
   - If it is running, gracefully terminate the existing process.
   - Start a new instance of `/home/user/secure_api.py` in the background.
   - Write the process ID (PID) of the newly started server to `/home/user/api.pid`.
   Make sure the script is executable (`chmod +x`). 

Ensure the server is running and accessible using the deployment script before you finish.