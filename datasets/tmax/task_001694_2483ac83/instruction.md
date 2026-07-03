You are an infrastructure engineer automating the provisioning of a lightweight, secure logging service. We have a specification diagram provided as an image that contains the required network port and authentication token for the service.

Your task involves three main steps:

1. **Information Extraction:**
   An image located at `/app/config_spec.png` contains the required configuration in the format:
   `PORT: <number>`
   `TOKEN: <secret_string>`
   Use `tesseract` to extract this information.

2. **Idempotent Provisioning Script:**
   Write a Bash script at `/home/user/provision.sh` that sets up and manages the lifecycle of this service. The script must be strictly idempotent (safe to run multiple times without causing errors or duplicating processes).
   The script must:
   - Create the directory `/home/user/service_data`.
   - Create a Python 3 HTTP server script at `/home/user/service_data/server.py` that listens on all interfaces (`0.0.0.0`) on the port extracted from the image.
   - The Python server must implement a `GET /` endpoint. If the HTTP request includes the header `Authorization: Bearer <secret_string>` (using the token from the image), it should return HTTP 200 with the body `Authorized`. Otherwise, it should return HTTP 401.
   - Start the Python server in the background and record its PID in `/home/user/service_data/server.pid`. All output (stdout and stderr) from the server must be appended to `/home/user/service_data/access.log`.
   - If the script is run while the server is already running (check via the PID file), it should do nothing and exit gracefully. If the PID file exists but the process is dead, it should clean up the PID file and restart the server.

3. **Log Configuration:**
   The `provision.sh` script must also generate a logrotate configuration file at `/home/user/service_data/logrotate.conf`. This configuration should target `/home/user/service_data/access.log` with the following settings:
   - Rotate daily
   - Keep 3 rotations
   - Compress the rotated files
   - Create new log file with permissions `0644`

Finally, execute your `/home/user/provision.sh` script to ensure the service is running and correctly provisioned. Do not leave the script running in the foreground; it must exit while leaving the server running in the background.