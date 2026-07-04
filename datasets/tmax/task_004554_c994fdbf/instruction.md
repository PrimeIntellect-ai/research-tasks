You are a Linux systems engineer responsible for hardening a local metric reporting service and setting up its deployment pipeline.

We have received a configuration specification as an image file located at `/app/network_spec.png`. This image contains two critical pieces of information for the new service:
1. The listening port (labeled as `PORT: <number>`)
2. The authentication token (labeled as `TOKEN: <string>`)

Your task is to build, deploy, and monitor this service using the following steps:

1. **Service Implementation (C):**
   Write a C program in `/home/user/src/server.c` that acts as a simple HTTP server. 
   - It must listen on `0.0.0.0` using the exact port recovered from the image.
   - It must handle incoming HTTP `GET /status` requests.
   - If the request includes the HTTP header `Authorization: Bearer <TOKEN>` (using the exact token from the image), it must respond with an HTTP 200 OK status and the exact body `OK\n`.
   - If the header is missing or incorrect, it must respond with HTTP 401 Unauthorized.
   - The server must run continuously and handle multiple sequential connections.

2. **CI/Build Automation:**
   Create a `Makefile` in `/home/user/src/` that contains a `deploy` target. Running `make deploy` should:
   - Compile `server.c` using `gcc`.
   - Place the compiled executable at `/home/user/bin/metric_server` (create the directory if it doesn't exist).

3. **Process Monitoring & Automation:**
   Since you do not have root access for systemd system services, create a custom watchdog script at `/home/user/bin/watchdog.sh`.
   - The script must check if the `metric_server` process is running.
   - If it is not running, the script should start `/home/user/bin/metric_server` in the background.
   - Make sure the script is executable.
   - Configure the user's crontab to run `/home/user/bin/watchdog.sh` every minute.

Once you have completed these steps, run `make deploy` and execute the watchdog script once manually to ensure the service is running before you finish.