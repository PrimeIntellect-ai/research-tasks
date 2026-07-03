You are a QA engineer setting up an automated testing environment for a legacy OCR service. The service pipeline consists of a C library that performs OCR (using a wrapper around tesseract), a Rust CLI tool that interfaces with the C library for safety, a Bash script that serves the Rust tool over HTTP, and an Nginx reverse proxy. 

Unfortunately, the environment is currently broken. You need to fix the components and bring up the service.

Here are your tasks:

1. **Fix the C Library**:
   - Location: `/app/c_src/`
   - The `Makefile` is broken and fails to build a shared library. Fix it so it correctly compiles `libocr.c` into a shared library named `libocr.so`.
   - `libocr.c` has a few compilation errors (missing headers, incorrect pointer usage). Fix them so it compiles cleanly.

2. **Fix the Rust Wrapper**:
   - Location: `/app/rust_src/`
   - The Rust project uses FFI to call `extract_text` from `libocr.so`. 
   - `src/main.rs` contains borrow checker and lifetime errors related to handling the C string returned by the FFI. Fix these errors so the project builds successfully with `cargo build`.
   - The Rust tool takes one argument (the image file path) and prints the extracted text to stdout.

3. **Create the Bash HTTP Server**:
   - Write a Bash script at `/app/server.sh` that starts a simple HTTP server listening on port `8081`. 
   - You can use `socat` or `nc` to handle incoming TCP connections. 
   - Whenever it receives an HTTP GET request (on any path), it should run the compiled Rust binary (`/app/rust_src/target/debug/rust_ocr`) and pass it the image file located at `/app/test_receipt.png`. 
   - It must return a valid HTTP 200 response where the body is the exact output of the Rust OCR tool.

4. **Configure Reverse Proxy**:
   - Create an Nginx configuration file at `/app/nginx.conf`.
   - The Nginx server must listen on port `8080` and proxy all HTTP requests to your Bash server on port `8081`.
   - Start Nginx in the background using your configuration file.

Ensure that both your Bash server and the Nginx proxy are running in the background. An automated verifier will send an HTTP GET request to `http://127.0.0.1:8080/` to ensure the system processes the image and returns the correct extracted text.