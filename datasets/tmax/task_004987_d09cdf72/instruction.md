You are tasked with executing a critical credential rotation for our legacy internal application suite. The application consists of an Nginx reverse proxy, a Flask web backend, a Redis session store, and a legacy custom C++ Authentication Daemon. 

Currently, the Flask app authenticates to Redis using an old, weak legacy password. Unfortunately, the documentation was lost, and the only artifact we have is a SHA-256 hash of this 6-character numeric pin (stored in `/home/user/app/legacy_hash.txt`). 

Your objectives are as follows:

1. **Password Recovery & Tooling (C++)**:
   Write a highly optimized C++ program located at `/home/user/app/recover_pin.cpp` that cracks the SHA-256 hash to find the 6-digit numeric pin. Compile it to `/home/user/app/recover_pin`. This tool must be highly efficient; our automated verification will test its speed against a large batch of hashes. It must read a hash from stdin, print ONLY the recovered plaintext pin to stdout, and exit.

2. **Service Auditing & Credential Rotation**:
   Once you have recovered the legacy pin, you must rotate the credentials. 
   - Generate a new secure 16-character alphanumeric password.
   - Update the Redis configuration located at `/home/user/app/redis/redis.conf` to use this new password.
   - Update the Flask application environment variables in `/home/user/app/flask/.env` to connect using the new Redis password.

3. **Network Policy Configuration**:
   The custom Authentication Daemon is currently exposing an unauthenticated debugging port on 8081. Update the Nginx configuration located at `/home/user/app/nginx/nginx.conf` to explicitly block (return 403) any external requests routed to `/auth-debug/`, while ensuring `/api/` traffic correctly proxies to the Flask app and `/auth/` proxies to the Auth Daemon.

4. **Integration**:
   Ensure all services (Nginx, Flask, Redis, and Auth Daemon) can successfully restart and communicate using the new credentials. Create a log file at `/home/user/app/rotation_report.txt` containing:
   Line 1: The old legacy pin
   Line 2: The newly generated secure password

Your solution will be evaluated on the correctness of the end-to-end flow and the execution speed of your C++ brute-force utility.