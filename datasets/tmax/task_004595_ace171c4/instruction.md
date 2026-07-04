I am acting as a cloud architect migrating a legacy microservice to a new local deployment pipeline. Currently, our local Nginx reverse proxy is returning a 502 Bad Gateway error because the upstream socket path is misconfigured, and our service management process is non-existent.

I need you to fix the configuration, create a service management script, and build a mock CI/CD deployment script.

Here is what you need to do:

1. **Fix the Nginx Configuration**:
   An Nginx configuration file is located at `/home/user/nginx/nginx.conf`. It is currently configured to route traffic to a legacy UNIX socket (`/tmp/legacy.sock`). Update the `upstream backend` block in this file to point to the new socket location: `/home/user/app.sock`. Do not modify any other Nginx settings.

2. **Create a Service Manager (`/home/user/manage_service.sh`)**:
   Write a bash script at `/home/user/manage_service.sh` to manage the lifecycle of our backend python service (`/home/user/app/backend.py`).
   The script must accept exactly one argument: `start`, `stop`, or `restart`.
   - `start`: Must set the environment variable `APP_SOCK=/home/user/app.sock`, launch `python3 /home/user/app/backend.py` in the background, and write its process ID to `/home/user/app.pid`.
   - `stop`: Must read the PID from `/home/user/app.pid`, cleanly terminate the process (using `kill`), and remove the pid file and the socket file (`/home/user/app.sock`).
   - `restart`: Must execute `stop` followed by `start`.
   Make sure the script is executable.

3. **Construct a CI/CD Deployment Hook (`/home/user/deploy.sh`)**:
   Write a script at `/home/user/deploy.sh` that simulates a deployment pipeline. The script must perform the following actions in order:
   - Call `/home/user/manage_service.sh restart` to ensure the backend is running fresh.
   - Start Nginx using the fixed configuration by running: `nginx -p /home/user/nginx -c /home/user/nginx/nginx.conf` (If Nginx is already running, this step should reload it using `nginx -p /home/user/nginx -s reload`).
   - Sleep for 2 seconds to allow services to initialize.
   - Run a health check by issuing an HTTP GET request to `http://localhost:8080/api` using `curl` and append the HTTP response body to a log file at `/home/user/migration.log`.
   Make sure the script is executable.

4. **Execute the Deployment**:
   Run your `/home/user/deploy.sh` script so that the system is fully started and the `/home/user/migration.log` file is generated.

Do not assume root privileges; all files and services must be created and run as the standard `user`. Nginx is configured to use unprivileged ports and local directories.