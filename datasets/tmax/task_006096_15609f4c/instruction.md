You are helping a developer migrate a legacy Python 2 web server to Python 3, while replacing its performance-critical string processing bottleneck with a Rust FFI extension.

The workspace is located at `/home/user/migration`. 
There are three main components to this task:

1. **Rust FFI & Borrow Checker Debugging**:
   In `/home/user/migration/rust_ext/src/lib.rs`, there is a Rust function `reverse_string` intended to be exported to C/Python. However, it currently has a memory/borrow checker issue (returning a dangling pointer).
   - Fix the Rust code so it correctly leaks the string into a raw pointer (e.g., using `into_raw()`) to be safely returned across the FFI boundary.
   - Build the Rust project in release mode (`cargo build --release`).

2. **Python 2 to Python 3 Migration & FFI Integration**:
   There is a legacy Python 2 script at `/home/user/migration/legacy_app.py`.
   - Migrate this script to Python 3, saving the new version as `/home/user/migration/app.py`.
   - Replace the pure Python `reverse_string` logic with a `ctypes` call to the compiled Rust shared library (`/home/user/migration/rust_ext/target/release/librust_ext.so`).
   - The Python server must listen on `127.0.0.1:8000`. It handles GET requests and expects a `text` query parameter.

3. **Reverse Proxy & Testing**:
   - Create an Nginx configuration file at `/home/user/migration/nginx.conf`. It should configure Nginx to run as a non-root user (do not use default system paths for pid/logs that require root), listen on `127.0.0.1:8080`, and reverse-proxy all requests to the Python server at `127.0.0.1:8000`.
   - Start your `app.py` in the background.
   - Start Nginx using your config (`nginx -c /home/user/migration/nginx.conf`).
   - Write a pytest file at `/home/user/migration/test_app.py` that tests the `app.py` FFI wrapper function (you can import it).
   - Finally, execute a curl request to the Nginx proxy: `curl "http://127.0.0.1:8080/?text=migration" > /home/user/migration/final_output.log`.

Make sure all services are running and the log file `final_output.log` is populated with the correct reversed string before you finish.