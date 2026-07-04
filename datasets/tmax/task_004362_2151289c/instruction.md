You are a support engineer tasked with investigating a critical deadlock in our production caching service. We've received reports that the system occasionally hangs completely under specific conditions.

We have exported the environment to `/app/`. The architecture consists of three composed services:
1. An Nginx reverse proxy
2. A Rust-based API service (using Tokio and Axum)
3. A Redis cache

Your objectives are:

**1. Memory Dump Analysis & MRE Creation**
A crash dump from the stalled Rust process is located at `/app/diagnostics/worker_memory.dump`. The logs indicated that the deadlock consistently occurs when processing a specific diagnostic payload. 
- Analyze the memory dump to find the offending payload string. It is a 32-character alphanumeric string that always follows the prefix `DIAG_PAYLOAD=`.
- In `/app/rust_api/tests/regression_test.rs`, write a minimal reproducible example (MRE) as a standard Rust integration test that sends this exact payload to the API and reproduces the hang (or would, if it weren't fixed).

**2. Deadlock Resolution**
The Rust API code is in `/app/rust_api/src/main.rs`. Identify the root cause of the deadlock. The engineers suspect it has to do with how `std::sync::RwLock` or `std::sync::Mutex` is being used across asynchronous await points or in improper orders.
- Modify `/app/rust_api/src/main.rs` to fix the concurrency bug. The application must process all payloads concurrently without hanging.

**3. Environment Integration**
The setup scripts failed to link the Nginx proxy to the Rust application. 
- Edit `/app/nginx/nginx.conf` to correctly proxy traffic from Nginx (which must listen on port 8080) to the Rust API (which runs on port 3000).
- Ensure the Rust app correctly points to the Redis instance on port 6379.
- Start all three services in the background. Nginx must listen on `127.0.0.1:8080`. 

**Verification:**
Once you have fixed the code, write a startup script at `/home/user/start_services.sh` that builds the Rust application and starts Redis, the Rust API, and Nginx. 
Ensure your script exits successfully and leaves the services running in the background. The automated verifier will execute this script, wait for the services to become healthy, and then fire HTTP requests (including the extracted diagnostic payload) against `127.0.0.1:8080/process` to verify the deadlock is resolved and the services are integrated correctly.