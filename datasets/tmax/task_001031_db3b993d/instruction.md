As a Site Reliability Engineer, we need to deploy a highly optimized, lightweight monitoring agent written in Go to track the uptime of our internal services. 

Our environment has two services running (simulated by a startup script you can run via `/app/start_services.sh`):
1. An Nginx reverse proxy listening on `127.0.0.1:8080`
2. A backend API listening on `127.0.0.1:8081`

Your task is to:
1. Write a Go program at `/app/monitor.go` that performs a single HTTP GET request to `http://127.0.0.1:8080/health` and `http://127.0.0.1:8081/health`.
2. The program must write the HTTP status codes to `/app/status.txt` exactly in this format on a single line: `nginx: <status>, api: <status>` (e.g., `nginx: 200, api: 200`).
3. Compile the Go program to a binary located at `/app/monitor`.
4. Because we deploy this to storage-constrained edge nodes, you must optimize the compilation of your Go binary so that its file size is as small as possible. The final binary size must be less than or equal to 3,000,000 bytes.
5. Create an idempotent cron configuration file at `/app/crontab.conf` that schedules `/app/monitor` to run every minute. Apply this crontab for the current user.

Ensure the backend services are running while testing your Go monitor. The final verification will check the binary size of `/app/monitor`, the contents of `/app/status.txt`, and the active crontab.