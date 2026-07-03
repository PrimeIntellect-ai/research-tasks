We have a simulated background application located in `/home/user/app` that is part of our local CI/CD deployment pipeline. Currently, our deployment script `/home/user/deploy.sh` tries to start the application, but it immediately fails and exits.

Your tasks are to:
1. Diagnose why the application (`/home/user/app/start.sh`) fails to start. You will discover that a symbolic link in the application's directory structure is broken/incorrect.
2. Fix the symbolic link so that it correctly points to `/home/user/shared_data`.
3. Create a health check script in any language of your choice at `/home/user/health_check` (e.g., `.sh`, `.py`, etc.). This script must perform an HTTP GET request to `http://127.0.0.1:8080/ping`.
4. If the endpoint successfully returns the text `pong` (with a 200 OK status), your health check script must append the exact string `STATUS: OK` to `/home/user/health.log`.
5. Execute `/home/user/deploy.sh` to successfully deploy and start the application.
6. Run your health check script to verify the application is running and to generate the required log entry in `/home/user/health.log`.

Note: You do not need root access for this task. Ensure that `/home/user/health.log` is created and contains the correct status message when your health check runs successfully.