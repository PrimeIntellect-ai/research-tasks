You are a Site Reliability Engineer responsible for ensuring our uptime monitoring stack is functioning correctly and writing a high-performance log parser for our analytics pipeline.

Our stack consists of three services running locally under your user:
1. **Nginx** (Reverse Proxy): Listens on `127.0.0.1:8080`. Its active configuration is located at `/home/user/nginx/nginx.conf`, and its PID file is at `/home/user/nginx/nginx.pid`.
2. **Backend Application**: Listens on `127.0.0.1:8081` and responds to `GET /ping` with a 200 OK.
3. **Health Checker**: Continuously polls `http://127.0.0.1:8080/ping` and writes the results to `/home/user/logs/health.log`.

Currently, the health checker is failing because Nginx is not routing the `/ping` endpoint to the backend correctly. We manage Nginx configuration via a local Git repository.

Your objectives:

**Part 1: Service Configuration & Git Hooks**
1. We have a bare Git repository at `/home/user/nginx.git` and a working clone at `/home/user/nginx-repo`.
2. In the clone, edit `nginx.conf` to correctly route requests for `/ping` to `http://127.0.0.1:8081/ping`.
3. Create a Git hook in the bare repository (`/home/user/nginx.git/hooks/post-receive`) so that whenever changes are pushed, it automatically:
   - Checks out the latest `nginx.conf` to `/home/user/nginx/nginx.conf`.
   - Sends a `SIGHUP` signal to the Nginx process using the PID file to reload the configuration gracefully.
4. Commit your changes in `/home/user/nginx-repo` and push them to the `origin` bare repository. Wait a few seconds to ensure `/home/user/logs/health.log` starts recording successful `UP` checks.

**Part 2: Log Parser implementation**
The health checker writes logs in the following format:
`YYYY-MM-DD HH:MM:SS | STATUS | LATENCY_MS`
Example:
```
2023-10-04 12:00:00 | UP | 45
2023-10-04 12:00:05 | DOWN | -1
```

You must write a log parser executable at `/home/user/parser` (you can use Python, Bash, Node, Ruby, etc. Ensure it has the executable bit set and an appropriate shebang). 
The parser must accept a single command-line argument: the path to a log file.
It must parse the file line by line and output exactly 5 bytes to standard output (stdout) for each line:
- **Byte 1**: `0x01` if STATUS is `UP`, `0x00` if STATUS is `DOWN`.
- **Bytes 2-5**: The `LATENCY_MS` encoded as a 32-bit unsigned integer in little-endian byte order. (If the status is `DOWN`, the latency in the file might be `-1`; you must encode it as `0`).

Your program must process the file efficiently and accurately, outputting nothing but the binary sequence. It will be rigorously tested against thousands of randomly generated log files.