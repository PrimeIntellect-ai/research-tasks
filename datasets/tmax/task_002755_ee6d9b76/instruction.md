You are a systems programmer debugging a C library issue for a new binary protocol backend. 

Your workspace is located at `/home/user/protocol_backend`. It contains a C project that compiles a shared library for serialization/deserialization, a simple TCP server relying on this library, and an Nginx reverse proxy configuration.

Currently, the project is broken. Your goals are:

1. **Fix the Linking Issue**: Run `make` in `/home/user/protocol_backend`. You will see a linking error (`multiple definition`) when building the shared library `libproto.so`. Diagnose and fix the C source code/headers so that `make` succeeds without warnings or errors.
2. **Configure the Reverse Proxy**: Edit `/home/user/protocol_backend/nginx.conf`. Configure it so that Nginx listens on port 8080 and acts as a reverse proxy, forwarding all HTTP requests to `127.0.0.1:9090` (where the C backend listens).
3. **Property-Based Testing**: Write a Bash script at `/home/user/protocol_backend/prop_test.sh`. This script must:
    * Generate 100 random alphanumeric strings of varying lengths (between 1 and 64 characters).
    * For each string, use `curl` to send a POST request to `http://127.0.0.1:8080/` with the string as the request body.
    * Compare the HTTP response body to the original string. The C server deserializes and re-serializes the payload; if the library works, the output must perfectly match the input.
    * If any mismatch occurs, print `FAIL: <input>` and exit with code 1.
    * If all 100 tests pass, print `PASS: ALL` and exit with code 0.
    * Ensure the script is executable (`chmod +x`).

To test your full setup:
1. Compile the project using `make`.
2. Start the backend: `./server &`
3. Start nginx using your config: `nginx -c /home/user/protocol_backend/nginx.conf`
4. Run your property tests: `./prop_test.sh`

Leave the server and Nginx running, and ensure `prop_test.sh` works correctly and prints `PASS: ALL`.