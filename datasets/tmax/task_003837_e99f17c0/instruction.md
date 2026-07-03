We are trying to deploy a Rust-based web service, but our Nginx reverse proxy is currently returning a 502 Bad Gateway error. 

The system consists of two services:
1. A local Nginx instance configured via `/home/user/nginx/nginx.conf` and listening on `127.0.0.1:8080`.
2. A Rust web service located in `/home/user/app/`. The compiled binary is at `/home/user/app/target/release/server`.

The issue was caused by a faulty deployment script. The startup script for the Rust app is failing to bind to the correct network location because of environment variable issues (it relies on a `.env` file but reads it from the wrong directory context, causing it to fall back to a default port of 9999, while Nginx expects it on port 8081).

Your task is to:
1. Diagnose and fix the environment or configuration so that the Rust service binds to `127.0.0.1:8081`.
2. Create an idempotent deployment shell script at `/home/user/deploy.sh` (ensure it is executable). This script must:
   - Gracefully terminate any existing Rust `server` process.
   - Start the Rust service in the background so it binds to the correct port.
   - Wait briefly for the Rust service to become available.
   - Perform a zero-downtime graceful reload of the local Nginx instance using the existing config file (`nginx -c /home/user/nginx/nginx.conf -s reload`).
3. Execute your `deploy.sh` script to bring the system to a healthy state.

When you are done, an automated verifier will make a `GET` request to `http://127.0.0.1:8080/health`. It must receive a `200 OK` response with the body `{"status":"ok"}`.