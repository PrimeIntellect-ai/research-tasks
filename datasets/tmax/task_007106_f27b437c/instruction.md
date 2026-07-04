You are a platform engineer responsible for maintaining a CI/CD pipeline. Our latest Python web service relies on a highly performant Rust core module (`rust_ext`). However, a recent commit broke the pipeline: the Rust module fails to compile due to ownership and borrow checker errors, the property-based tests are missing, and the local reverse proxy setup for integration testing hasn't been configured.

Your task is to fix the application, add property-based testing, and stand up the reverse proxy for testing.

Here are your specific requirements:

1. **Fix the Rust Bug:** 
   The Rust extension is located at `/home/user/workspace/rust_ext`. Inside `/home/user/workspace/rust_ext/src/lib.rs`, there is a function called `process_string` which is supposed to take a string and concatenate it to itself (e.g., "abc" becomes "abcabc"). It currently has a borrow checker issue. Fix the Rust code so that it compiles and performs the concatenation correctly. 
   Once fixed, build and install the module into your environment using `maturin develop` inside the `rust_ext` directory.

2. **Property-Based Testing:**
   Create a test file at `/home/user/workspace/test_ext.py`. Use the `hypothesis` Python library to write a property-based test for `rust_ext.process_string`. 
   The test function must be named `test_process_string_property` and use `hypothesis.strategies.text()` to verify that for any string `s`, `rust_ext.process_string(s)` equals `s + s`.
   Run the test with `pytest /home/user/workspace/test_ext.py` to ensure it passes. You do not need to save the test output, but the file must exist and pass.

3. **Reverse Proxy Configuration:**
   We use Nginx to reverse proxy requests to our Flask app during integration tests. 
   Create an Nginx configuration file at `/home/user/workspace/nginx.conf`. 
   The configuration must:
   - Run in the foreground or background (your choice), but do not require root. Use `pid /home/user/workspace/nginx.pid;` and configure `error_log` and `access_log` to point to `/home/user/workspace/`.
   - Set the `worker_processes` to 1.
   - Include an `events` block.
   - Include an `http` block with a `server` that listens on port `8080`.
   - Route all requests (`location /`) to `http://127.0.0.1:5000` (where the Flask app will run).

4. **Integration Run:**
   - A Flask app is already provided at `/home/user/workspace/app.py`. Start it in the background (`python /home/user/workspace/app.py &`).
   - Start Nginx using your config: `nginx -c /home/user/workspace/nginx.conf &`.
   - Wait for the services to be ready, then test the proxy by sending a GET request: `curl -s "http://127.0.0.1:8080/process?text=platform"`.
   - Save the exact string response from that `curl` command into a file located at `/home/user/workspace/response.txt`.

Ensure all files are precisely located at `/home/user/workspace/` as requested.