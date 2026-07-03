You are a developer tasked with fixing a broken multi-service backend environment. In `/home/user/app`, there is a setup containing a Rust-based REST API and an Nginx configuration. Currently, the Rust project fails to compile, the API lacks the final implementation for a numerical algorithm, and the services are not properly integrated.

Your goals are as follows:

1. **Fix and Complete the Rust API (`/home/user/app/rust_api`)**:
   - The Rust project uses `actix-web`. It is supposed to expose a REST endpoint at `POST /api/matrix_pow`.
   - The endpoint accepts a JSON payload containing a 2x2 integer matrix and a power `n` (e.g., `{"matrix": [[1, 1], [1, 0]], "n": 10}`).
   - It should return the matrix raised to the power of `n` using fast exponentiation (binary exponentiation) in JSON format: `{"result": [[89, 55], [55, 34]]}`.
   - Currently, `src/main.rs` and `src/math.rs` have compilation errors (type mismatches, missing imports, and incomplete parsing logic). Fix the compilation errors and complete the matrix exponentiation algorithm in `src/math.rs`.

2. **Configure Nginx (`/home/user/app/nginx.conf`)**:
   - Edit the Nginx configuration file provided.
   - Nginx must listen on `127.0.0.1:9000`.
   - It must proxy all requests starting with `/api/` to the Rust API, which should be configured to run on `127.0.0.1:8080`.

3. **Service Orchestration**:
   - Build and start the Rust API in the background. It must listen on `127.0.0.1:8080`.
   - Start Nginx using the configuration file at `/home/user/app/nginx.conf`.
   - Write a short log file to `/home/user/app/startup.log` containing the text "SERVICES_READY" once both processes are running and actively listening on their respective ports.

Make sure both services remain running in the background so they can be tested. Ensure your matrix exponentiation implementation handles `n=0` by returning the identity matrix. Do not use external mathematical crates for the matrix multiplication; implement it manually.