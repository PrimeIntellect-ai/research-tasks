You are an observability engineer investigating a simulated 502 Bad Gateway incident on a local user-space reverse proxy. Your monitoring dashboard indicates that the reverse proxy is unable to communicate with its backend service due to a mismatched Unix socket configuration.

Your task consists of three parts: analyzing the configuration, remediating the issue, and implementing a health check script.

1. **Configuration Remediation**:
   - Inspect the Nginx configuration located at `/home/user/app/nginx.conf`. You will notice an `upstream` or `proxy_pass` directive pointing to an incorrect Unix socket path.
   - Inspect the backend service environment configuration file at `/home/user/app/backend.env`. This file contains an environment variable `LISTEN_SOCKET` which defines the true path where the backend service binds its Unix socket.
   - Update `/home/user/app/nginx.conf` to use the correct socket path derived from `/home/user/app/backend.env`. Ensure you maintain the correct Nginx syntax (e.g., `proxy_pass http://unix:/path/to/socket;`).

2. **Health Check Implementation**:
   - Write a Bash script at `/home/user/monitor.sh`.
   - The script must parse `/home/user/app/nginx.conf`, extract the configured Unix socket path from the `proxy_pass` directive, and check if that file path exists on the filesystem.
   - If the extracted socket file exists, the script must append exactly: `STATUS: HEALTHY - <extracted_path>` to `/home/user/app/metrics.log`.
   - If the socket file does not exist, it must append exactly: `STATUS: UNHEALTHY - <extracted_path>` to `/home/user/app/metrics.log`.
   - Ensure the script `/home/user/monitor.sh` has executable permissions.

Do not start any long-running daemon processes; simply configure the files and write the script as requested. Provide no interactive output; we will test your script by executing `/home/user/monitor.sh` and reading `/home/user/app/metrics.log`.