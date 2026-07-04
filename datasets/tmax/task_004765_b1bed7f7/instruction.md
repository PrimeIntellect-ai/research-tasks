We have a local web service stack that is currently failing with a "502 Bad Gateway" error. The stack consists of a local Nginx instance (running as an unprivileged user) reverse-proxying to a custom Rust backend service. 

Your objective is to fix the 502 error, ensure the Rust backend is functioning correctly according to its intended logic, and set up a health monitoring script.

Here are the details of the environment and what you need to do:

1. **Fix the Nginx Configuration and 502 Error:**
   - Nginx is installed, and a user-specific configuration is located at `/home/user/nginx.conf`. It is supposed to listen on port `9090` and proxy requests to the Rust backend running locally on port `8080`.
   - Start the unprivileged Nginx instance using this configuration. Debug why it is returning a 502 Bad Gateway when you run `curl http://127.0.0.1:9090/process` and fix the integration.

2. **Fix the Vendored Rust Backend:**
   - The source code for the Rust backend is provided in `/app/rusty-slugger-1.2.0`. 
   - It is an HTTP server that takes a plaintext string via a POST request, converts it into a URL-friendly slug, and returns the result. It can also run as a CLI tool if passed a string argument.
   - The application has a bug: it currently panics on startup because of a missing required environment variable related to the monitoring primitive, and its slug-generation logic was recently broken by a bad patch (it drops numeric characters instead of preserving them).
   - Fix the code in `/app/rusty-slugger-1.2.0/src/main.rs` so that it successfully binds to `127.0.0.1:8080` and preserves numbers in slugs (e.g., "Hello World 123" should become "hello-world-123").
   - Compile the fixed application and copy the final executable to `/home/user/backend-bin`. Run this binary in the background so Nginx can reach it.

3. **Container & Process Lifecycle Monitoring:**
   - Create a health check script at `/home/user/health.sh`.
   - The script should send a POST request with the body "health check 1" to `http://127.0.0.1:9090/process`. 
   - If the response is exactly "health-check-1", it should exit with code 0. Otherwise, it should exit with code 1. Make sure the script is executable.

You may test your logic against Nginx to ensure the 502 error is gone and the slugging service works as expected.