You are tasked with setting up a local CI/CD deployment pipeline for a secure Go web service. The service simulates sending email alerts and relies on specific timezone configurations for its logging. Because you do not have root access, you will orchestrate this entirely within the user's home directory.

Please perform the following steps to complete the setup:

1. **Directory Structure & Configuration**
Create the following directories:
- `/home/user/app`
- `/home/user/certs`
- `/home/user/config`
- `/home/user/mailbox`

Create a configuration file at `/home/user/config/settings.json` with the following exact JSON content:
```json
{"admin_email": "sysadmin@local.domain"}
```

2. **The Go Web Server (`/home/user/app/server.go`)**
Write a Go web server in `/home/user/app/server.go` that does the following:
- On startup, it must append a line to `/home/user/app/startup.log`. The line must be the current time formatted exactly as RFC3339. Crucially, the time must be recorded in the `Europe/Copenhagen` timezone.
- It must listen for HTTPS traffic on `127.0.0.1:9443` using TLS certificates located at `/home/user/certs/cert.pem` and `/home/user/certs/key.pem`.
- **Endpoint `/health`**: Responds with HTTP 200 and the JSON payload `{"status": "ok"}`.
- **Endpoint `/notify`**: When a GET request is made, it reads the `admin_email` from `/home/user/config/settings.json`. It then creates (or overwrites) a mock email file at `/home/user/mailbox/alert.eml` with the exact following content:
```text
To: [admin_email from settings.json]
Subject: Alert

Service notification triggered.
```
After writing the file, it should respond with HTTP 200.

3. **The CI/CD Deployment Script (`/home/user/deploy.sh`)**
Write a bash script at `/home/user/deploy.sh` (ensure it is executable) that performs the following automated deployment steps:
- Generates a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`) in `/home/user/certs/`. The certificate should be valid for `127.0.0.1`.
- Compiles the Go server (`/home/user/app/server.go`) into an executable named `/home/user/app/server`.
- Ensures the `TZ` environment variable is exported and set to `Europe/Copenhagen` for the server process.
- Starts the compiled `/home/user/app/server` in the background.
- Waits for 2 seconds to allow the server to start.
- Uses `curl` to make an insecure (`-k` / `--insecure`) GET request to `https://127.0.0.1:9443/notify` to trigger the email generation.

Execute `/home/user/deploy.sh` so the server is running and the `alert.eml` file is generated. Leave the server running in the background.