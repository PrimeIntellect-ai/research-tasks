You are an infrastructure engineer working on an automated provisioning and log processing system. You have two main objectives: fix a broken multi-service container setup and write a Python log processing utility that exactly matches our legacy specification.

Objective 1: Multi-Service Compose Fix
In `/app/`, there is a `docker-compose.yml` file defining a web server (Nginx) and a backend service. 
Currently, the setup is broken:
1. Nginx is configured to serve static content from `/var/www/html/` (via a volume mount from the host `/home/user/www`), but our deployment puts the static files in `/app/static`. You must use directory link management to create a symlink so that `/home/user/www` points to `/app/static` (you may need to remove the existing empty `/home/user/www` directory first).
2. The `docker-compose.yml` does not expose the Nginx port to the host. Modify the file to add port forwarding, mapping port 8080 on the host to port 80 on the Nginx container.
3. Start the container lifecycle (run `docker compose up -d` in `/app/`). Once successful, a request to `http://localhost:8080/index.html` should return the contents of the static file.

Objective 2: Log Processing Script
We need a fast log parsing script written in Python. 
Create a file at `/home/user/process_log.py`. The script will be called with a single command-line argument: a standard access log line string.
Example input:
`192.168.1.50 - - [10/Oct/2023:13:55:36 -0700] "GET /api/data HTTP/1.1" 200 1024`

Your script must parse this string using text processing and output a strictly formatted string:
`IP: <ip> | METHOD: <method> | PATH: <path> | STATUS: <status>`
For the example above, the output must exactly be:
`IP: 192.168.1.50 | METHOD: GET | PATH: /api/data | STATUS: 200`

If the status code is 400 or greater, you must append ` | ERROR` to the output.
Example input:
`10.0.0.1 - - [10/Oct/2023:14:00:00 -0700] "POST /login HTTP/1.1" 403 512`
Output:
`IP: 10.0.0.1 | METHOD: POST | PATH: /login | STATUS: 403 | ERROR`

Ensure your script handles standard Nginx log formats correctly. Automated tests will verify your Python script's behavior against an oracle implementation using hundreds of fuzzed log lines. Your output must be bit-exact.