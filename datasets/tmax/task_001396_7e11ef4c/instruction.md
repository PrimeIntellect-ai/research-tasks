You are an expert container specialist and systems administrator. We have a microservices architecture that processes timezone configurations, but the current deployment is broken and vulnerable to malicious payloads.

Your task is to fix the environment, deploy the services correctly, and write a robust filter to protect the backend.

### 1. Multi-Service Configuration
A startup script located at `/home/user/app/start_services.sh` launches three services:
- NGINX frontend
- API backend (Flask)
- Redis cache

Currently, they are not communicating correctly. You need to perform connectivity diagnostics and reconfigure the services so that:
- NGINX listens on port 8080 and proxies requests starting with `/api/` to the Flask backend.
- The Flask backend listens on port 5000 and connects to Redis on port 6379.
- Modify the configuration files in `/home/user/app/config/` (specifically `nginx.conf` and `backend.env`) to establish this end-to-end flow.
- Ensure the locale and timezone for the API service are set to `en_US.UTF-8` and `UTC` respectively via its environment file.

### 2. Timezone Payload Filter
The API receives timezone configuration files, but we've been receiving malicious payloads (e.g., path traversals, command injections).
Write a filter script in the language of your choice at `/home/user/filter_tz.sh` (or `.py`, `.js`, etc.) that takes a file path as an argument.
The script must exit with code `0` if the file is a clean, valid timezone configuration, and exit with code `1` if it is malicious.
A valid timezone file contains exactly one line with a valid IANA timezone string (e.g., `America/New_York`) consisting only of letters, numbers, underscores, dashes, and forward slashes.

### 3. Fstab Setup and Deployment
We simulate mounting data volumes using a custom fstab file. Create a file at `/home/user/app_fstab` containing a single line to bind-mount `/home/user/data_source` to `/home/user/app/data` using the `bind` option.
Then, write a robust deployment script at `/home/user/deploy.sh` that safely restarts the API service without dropping requests (simulate a staged deployment by waiting for the Redis cache to be ready before starting the API backend).

Your final output will be tested automatically.