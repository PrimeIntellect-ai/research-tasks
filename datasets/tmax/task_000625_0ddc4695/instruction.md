You are a system administrator tasked with diagnosing and fixing a multi-service application that is currently failing to start. 

Our application stack consists of three components managed by `supervisord` (acting as our process supervisor since user-level systemd is unavailable in this environment):
1. A Python Flask API service (`api-service`)
2. A storage monitoring daemon (`storage-monitor`)
3. An Nginx reverse proxy (`nginx`)

Currently, the `api-service` crashes immediately upon startup and enters a FATAL state. Furthermore, the Nginx reverse proxy is returning 502 Bad Gateway errors even when the API is manually started.

Your objectives are:
1. **Diagnose and Fix the API Service:** Inspect the supervisor logs in `/home/user/logs/` to determine why `api-service` is crashing. The service has a strict startup check related to its data directory (`/home/user/app_data/`). Resolve the underlying filesystem issue so the service can start successfully.
2. **Update Process Supervisor Policies:** Edit the supervisord configuration file at `/home/user/supervisor/supervisord.conf`. The `api-service` is currently configured to never restart on failure. Change its configuration so that `autorestart=true` and `startretries=5`.
3. **Fix the Reverse Proxy:** The Nginx configuration located at `/home/user/nginx/nginx.conf` is misconfigured. It should be listening on port 8080 and routing all traffic to the `api-service` running on `127.0.0.1:5000`. Fix the upstream routing configuration.
4. **Apply and Verify:** Reload `supervisord` to apply your configuration changes and start the services. Ensure that all processes (`api-service`, `storage-monitor`, and `nginx`) are in the RUNNING state using `supervisorctl`.

To complete the task, an automated verifier will issue HTTP requests to the Nginx reverse proxy on `127.0.0.1:8080`. It will verify:
- `GET http://127.0.0.1:8080/ping` returns an HTTP 200 with the text `pong`.
- `POST http://127.0.0.1:8080/data` returns an HTTP 200.

You must leave all services running in the background via `supervisord`.