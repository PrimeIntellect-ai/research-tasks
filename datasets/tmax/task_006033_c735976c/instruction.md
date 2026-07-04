You are a container specialist managing a local microservices stack. We have a Python-based backend service managed by `supervisord` that is currently failing to start and bind to its designated socket.

Your task is to fix the configuration and the code so the service runs properly:

1. **Fix the Python Application** (`/home/user/app.py`):
   - The script currently crashes with an "Address already in use" error if the socket file already exists from a previous run. Modify the script to robustly handle this by unlinking/removing the socket file before attempting to bind it.
   - Do not remove the timezone check in the script; it enforces that the correct timezone is set.

2. **Update Supervisor Configuration** (`/home/user/supervisord.conf`):
   - The Nginx proxy (not running in this task) expects the upstream socket to be located at `/home/user/app.sock`, but the supervisor config currently passes `/tmp/wrong.sock` to the application. Update the `command` in the `[program:myapp]` section to use `/home/user/app.sock`.
   - The application requires a specific timezone to operate. Configure the `[program:myapp]` section to inject the environment variable `TZ=Europe/Berlin`.
   - Ensure the `myapp` process is supervised properly by setting it to automatically restart if it crashes (`autorestart=true`).

3. **Run and Verify**:
   - Start the supervisor daemon using the updated configuration: `supervisord -c /home/user/supervisord.conf`
   - Ensure the service is running and serving requests on `/home/user/app.sock`.
   - Send an HTTP GET request to the Unix socket (e.g., using `curl --unix-socket /home/user/app.sock http://localhost/`) and redirect the raw response to `/home/user/success.log`. The test suite will check this log file to verify the service works.