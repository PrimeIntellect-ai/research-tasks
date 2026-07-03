You are a security auditor tasked with securing a multi-service web application environment located in `/app/`. The environment consists of an Nginx reverse proxy, a custom C-based application backend, and a Redis instance used for session management. 

Your goals are to verify and fix application file permissions, configure the services to communicate correctly, and develop a C-based algorithmic security filter to sanitize incoming requests based on security logs.

**Part 1: Permission Auditing**
The directory `/app/secure_data/` contains sensitive certificate chains (`server.crt`, `server.key`) and configuration files. They currently have overly permissive access rights. You must write a shell script `/home/user/fix_perms.sh` that sets the ownership of all files in `/app/secure_data/` to the `www-data` user, restricts permissions for `.key` files to `0400`, and `.crt` files to `0444`. Run this script.

**Part 2: Service Composition**
The application uses three services:
1. Nginx (listening on port 8080)
2. Custom C Backend (listening on port 9000)
3. Redis (listening on port 6379)

Currently, Nginx is not correctly forwarding requests to the C backend, and the backend cannot connect to Redis. 
Edit the Nginx configuration at `/app/config/nginx.conf` so that all requests to `/api/` are proxy-passed to `127.0.0.1:9000`. 
Edit the backend environment variables in `/app/config/backend.env` to point the `REDIS_HOST` variable to `127.0.0.1` and `REDIS_PORT` to `6379`.
Start all services using the provided `/app/start_services.sh` script.

**Part 3: Algorithmic Vulnerability Filter (C)**
The backend relies on a standalone log filtering tool to detect malicious payloads (Injection, XSS) and brute-force password attempts. 
Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`.
The program must read log entries from standard input (one entry per line). 
For each line, it must output exactly `ACCEPT` or `REJECT` followed by a newline.
- You must REJECT lines containing typical SQL injection patterns (e.g., `' OR '1'='1`, `UNION SELECT`) or XSS patterns (e.g., `<script>`, `onerror=`).
- You must REJECT IPs that appear more than 5 times consecutively attempting to access `/login` (brute-force detection).
- You must ACCEPT all other normal traffic.

You have been provided with two directories containing test corpora:
- `/app/corpus/clean/` contains logs of normal user behavior.
- `/app/corpus/evil/` contains logs with injection attacks and brute-force attempts.

Your compiled `/home/user/filter` must successfully process both corpora. A verification script will pipe files from these directories into your filter. You must achieve 100% rejection of the evil corpus and 100% acceptance of the clean corpus.

Finally, write the output of running your filter against `/app/corpus/evil/test_log_1.txt` into `/home/user/verification.log`.