We are implementing a configuration tracking system to monitor time-series changes across our microservices. A proprietary hashing tool is provided as a compiled binary, but the wrapper and ingestion server need to be built.

Your task is to build a configuration ingestion service and schedule its maintenance. 

1. **The Hashing Binary**
   You have been provided a stripped, packed binary at `/app/config_hasher`. It takes raw configuration text via standard input (`stdin`) and outputs a specific signature string to `stdout`.

2. **The Ingestion Server**
   Create a server (using any language of your choice) that listens on `127.0.0.1:9090`. It must accept HTTP POST requests to the `/track` endpoint with a JSON body of the following format:
   ```json
   {
     "timestamp": "2023-10-25T14:30:00Z",
     "service": "api-gateway",
     "config_data": "max_connections=100\ntimeout=30"
   }
   ```

3. **Data Validation**
   Upon receiving a request, your server must validate the payload:
   - `timestamp`: Must perfectly match ISO8601 format (e.g., `YYYY-MM-DDThh:mm:ssZ`).
   - `service`: Must strictly match the regex pattern `^[a-z0-9_-]{3,16}$`.
   - If any validation fails, the server must return an HTTP 400 Bad Request.

4. **Processing and Storage**
   If the payload is valid:
   - Pass the `config_data` strictly to the `/app/config_hasher` binary via stdin.
   - Read the resulting signature.
   - Append a single line to `/home/user/tracked_configs.log` in this exact format:
     `[{timestamp}] {service} | SIGNATURE: {signature}`
   - Return an HTTP 200 OK.

5. **Pipeline Scheduling**
   To ensure the log file doesn't grow indefinitely, write a crontab configuration file to `/home/user/log_rotate.cron`. This file should contain a single cron expression to execute `/usr/bin/logrotate -f /etc/logrotate.d/tracker` every day at exactly midnight (00:00). 

Ensure your server remains running in the background so it can be tested. You can use standard Linux CLI tools, shell scripts, Python, or any installed runtime to implement the server.