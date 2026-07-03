You are a log analyst investigating traffic patterns and system performance. You have been provided with a raw access log file and a simple Bash-based HTTP server. Your task is to process the log file, extract time series statistics, and serve the aggregated data via an HTTP API using the provided server.

Here are the requirements:

1. **Fix the HTTP Server:**
   - A third-party Bash HTTP server (`bashttpd`) is vendored at `/app/bashttpd-master`.
   - The server has an intentional bug preventing it from correctly parsing the HTTP request path (URI). You must find and fix this bug in the server's source code so it can correctly route requests.
   - Configure the server to serve requests using `socat` or `nc` as per the `bashttpd` documentation, listening on `127.0.0.1:8080`.

2. **Data Processing (Bash script expected):**
   - The raw log file is located at `/home/user/access.log`.
   - The log format is: `[YYYY-MM-DD HH:MM:SS] IP_ADDRESS "METHOD PATH HTTP/1.1" STATUS_CODE RESPONSE_TIME_MS`
   - First, remove any exactly duplicate log lines (some lines were duplicated due to a logging glitch).
   - Aggregate the cleaned log data by the minute (e.g., `YYYY-MM-DD HH:MM`).
   - For each minute, calculate:
     - `total_requests`: Total number of requests in that minute.
     - `error_count`: Total number of requests with a STATUS_CODE >= 400.
     - `avg_response_time`: Average response time in milliseconds (as an integer, rounded down to the nearest whole number).

3. **Output Format:**
   - Save the aggregated data to `/home/user/stats.json`.
   - The file must be a valid JSON array of objects, sorted chronologically by minute. Example format:
     ```json
     [
       {
         "minute": "2023-10-01 10:00",
         "total_requests": 42,
         "error_count": 2,
         "avg_response_time": 105
       },
       ...
     ]
     ```

4. **Serve the Data:**
   - Configure `bashttpd` to respond to `GET /stats`.
   - The response must have a `200 OK` status, a `Content-Type: application/json` header, and the body must be the exact contents of `/home/user/stats.json`.
   - Start the server in the background so it is actively listening on `127.0.0.1:8080` when your final command completes.

Use Bash as your primary tool for the data processing pipeline. Ensure your server is running and accessible before finishing.