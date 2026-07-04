You are tasked with building a lightweight, local "Validating Manifest Proxy" that mimics a Kubernetes validating webhook combined with a reverse proxy. It will silently intercept manifest submissions, reject unauthorized ones, and forward valid ones to a backend API. You also need to set up process monitoring and scheduling to ensure these services remain active.

All work must be done in `/home/user/manifest-operator`.

**Step 1: The Backend Dummy API**
Write a Go program named `backend.go`. 
- It must listen on `127.0.0.1:8081`.
- It must accept `POST` requests on the `/apply` endpoint.
- Whenever a request is received, it must return a `200 OK` status and append a line to `/home/user/manifest-operator/backend.log` with the exact format: `ACCEPTED: <length_of_body_in_bytes> bytes`.

**Step 2: The Validating Reverse Proxy**
Write a Go program named `proxy.go`.
- It must listen on `127.0.0.1:8080`.
- It must accept `POST` requests on the `/apply` endpoint.
- It must parse the incoming request body as JSON. 
- It must check if the JSON object contains a nested path: `metadata.annotations["proxy.local/managed"]`.
- If the value of this annotation is exactly `"true"`, it must reverse-proxy the unmodified request to the Backend Dummy API (`http://127.0.0.1:8081/apply`).
- If the JSON is invalid, the annotation is missing, or the value is not `"true"`, the proxy must silently reject the request by returning an HTTP `403 Forbidden` status and appending a line to `/home/user/manifest-operator/proxy.log` with the exact format: `REJECTED`. It must *not* forward the request to the backend.

**Step 3: Process Monitoring**
Write a bash script named `monitor.sh` in the same directory.
- This script must check if processes are currently listening on ports `8080` and `8081` (e.g., using `ss`, `netstat`, or `lsof`).
- If port `8081` is not listening, the script must compile and start `backend.go` in the background.
- If port `8080` is not listening, the script must compile and start `proxy.go` in the background.
- The script must be executable.

**Step 4: Scheduling**
Configure a user cron job that executes `/home/user/manifest-operator/monitor.sh` every minute. Ensure the cron job uses absolute paths.

Build and start the system (you can run `monitor.sh` manually to bootstrap it), then verify your cron job is installed.