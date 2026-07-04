You are the on-call engineer and have just been paged at 3 AM. Our internal job scheduling service, `bash-http-scheduler`, is failing to schedule jobs correctly, particularly for users in different timezones and for boundary times (e.g., exactly midnight).

The service is a custom Bash-based HTTP server vendored at `/app/bash-http-scheduler`. It relies on `socat` to handle TCP connections and uses Bash scripts to process HTTP POST requests for scheduling.

Users are reporting two issues:
1. Whenever they try to schedule a job using a UTC time that has already passed in the local server's timezone but is still in the future for UTC, the server rejects it. The server should treat all incoming schedule times as UTC, regardless of the local system timezone.
2. The server crashes/rejects requests when a job is scheduled with a time exactly 24 hours from the start of the current day. 

Your tasks:
1. Investigate the vendored source code in `/app/bash-http-scheduler`.
2. Fix the timezone parsing bug so that all incoming times are interpreted as UTC.
3. Fix the off-by-one boundary condition / assertion error that rejects valid edge-case times.
4. Ensure the server can be started via its `Makefile` (you may need to fix the Makefile or install missing dependencies like `socat`).
5. Start the service running in the background, listening on `127.0.0.1:8080`.

The service must accept an HTTP `POST /schedule` request with a payload like `time=15:30&job=test`. It should return a `200 OK` HTTP response with a body containing the scheduled Unix timestamp. 

You must leave the fixed service running on port 8080.