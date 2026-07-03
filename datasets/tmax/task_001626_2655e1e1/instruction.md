You are a storage administrator for a high-traffic web platform. Recently, a runaway module in the backend application has been filling up disk space with massive, multi-line spam logs. 

Your task is to implement a robust log sanitizer in C, pass our adversarial log corpus tests, and reconfigure the existing service pipeline to use your sanitizer to prevent disk space exhaustion.

**Part 1: The Log Sanitizer (C Implementation)**
Write a C program at `/home/user/log_sanitizer.c` and compile it to `/home/user/log_sanitizer`.
The program must take exactly two arguments: `<input_dir>` and `<output_dir>`.
It must perform the following operations:
1. Recursively traverse the `<input_dir>` and find all files ending in `.log`.
2. Parse the files into distinct multi-line log records. A new log record always starts with a timestamp exactly in this format: `[YYYY-MM-DD HH:MM:SS]` (e.g., `[2023-10-25 14:32:01]`). Any subsequent lines that do not start with this timestamp pattern are part of the preceding log record.
3. If a parsed log record contains the exact string `[SPAM-MODULE]` anywhere within its lines, the *entire* multi-line record must be discarded.
4. Clean records must be written to the corresponding relative path in `<output_dir>`. For example, `/in/app/web.log` should be written to `/out/app/web.log`.
5. To prevent the log shipper from reading partial files, writes to the output directory must be atomic (e.g., write to a temporary file like `web.log.tmp` first, then rename it to `web.log`).

**Part 2: The Adversarial Corpus Validation**
Your compiled `/home/user/log_sanitizer` must be perfectly accurate. Our automated verifier will test your binary against two corpora located at `/home/user/verifier/evil_corpus/` and `/home/user/verifier/clean_corpus/`.
You must ensure that 100% of the clean log records are preserved byte-for-byte, and 100% of the log records containing the spam payload are rejected.

**Part 3: Multi-Service Reconfiguration**
The application stack is located in `/home/user/app/` and consists of three services managed by a local startup script:
1. **Nginx** (Frontend Proxy, port 8080)
2. **Flask WebApp** (Backend API, port 5000)
3. **LogShipper** (Daemon reading from `/home/user/logs/processed/`)

Currently, the Flask WebApp is configured to write logs directly to `/home/user/logs/processed/`, which the LogShipper ingests immediately. 
You must:
1. Modify the WebApp's configuration file `/home/user/app/webapp/config.yaml` so that it writes its logs to `/home/user/logs/raw/` instead.
2. Modify `/home/user/app/nginx.conf` to add the HTTP header `X-Sanitizer-Enabled: true` to all requests forwarded to the backend. The WebApp requires this header to activate the new logging pipeline.
3. Restart the services using `/home/user/app/restart_services.sh`.
4. Run your `/home/user/log_sanitizer` manually once against `/home/user/logs/raw/` routing to `/home/user/logs/processed/` to ensure the end-to-end flow works and the LogShipper only sees clean data.

Leave your compiled binary at `/home/user/log_sanitizer` for the final verification step.