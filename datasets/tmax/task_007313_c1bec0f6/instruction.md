You are tasked with fixing and deploying a local token validation utility. This utility relies on a legacy C library for the actual cryptographic validation, wrapped by a Rust REST API. Finally, it must be exposed through a reverse proxy for security.

Your environment is set up in `/home/user/auth_util`. 

Here is what you need to do:

1. **Fix the Rust REST API (`/home/user/auth_util/api`)**
   The Rust API uses `axum` to expose a `/validate` endpoint and interfaces with a compiled C library (`libtoken.so`) using FFI. However, the original developer left a compilation error (a Rust ownership/borrow checker issue) in `src/main.rs`. 
   Fix the borrow checker error so the project compiles successfully via `cargo build --release`. Do not change the API endpoint path (`/validate`), the request/response JSON schema, or the FFI signature.

2. **Configure Nginx Reverse Proxy**
   Create an Nginx configuration file at `/home/user/auth_util/nginx.conf`.
   Nginx must:
   - Listen on port `8080`.
   - Reverse proxy all traffic from `/` to the Rust API (which runs on port `3000`).
   - Add a custom HTTP response header `X-Proxy-Secure: true` to all responses.
   - Block any requests to `/admin` (and its subpaths) by returning a `403 Forbidden` status.

3. **Create a Startup Script**
   Create an executable bash script at `/home/user/start.sh`.
   When executed, this script must:
   - Ensure the `LD_LIBRARY_PATH` includes `/home/user/auth_util/clib` so the Rust binary can find `libtoken.so`.
   - Start the compiled Rust API binary in the background.
   - Start Nginx in the background using your custom configuration (`nginx -c /home/user/auth_util/nginx.conf -g "daemon off;" &`).
   - The script should exit cleanly (returning 0) while leaving both background processes running.

The C library is already compiled and located at `/home/user/auth_util/clib/libtoken.so`. It exposes the following C signature:
`int validate_token(const char* token);` (returns 1 for valid, 0 for invalid).

Verify your setup. A POST request to `http://localhost:8080/validate` with `{"token": "SECURE_XYZ"}` should return `{"valid": true}` and have the `X-Proxy-Secure: true` header.