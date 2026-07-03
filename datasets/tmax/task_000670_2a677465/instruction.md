You are a platform engineer responsible for maintaining our CI/CD pipelines. We are implementing a new "Build Validation Gateway" to ensure that low-level initialization payloads (assembly code) submitted by developers are correctly formatted, assemble without errors, and are cryptographically bound to the current build ticket before deployment.

Your task is to create a Python-based REST API that acts as this validation gateway. 

Step 1: Extract Build Configuration
A scanned build ticket has been placed at `/app/build_ticket.png`. 
1. Use `tesseract` to extract the text from this image.
2. The image contains a configuration string in the format: `AUTH_SEED: <seed_value>`. Parse and securely store this `<seed_value>` in your application logic.

Step 2: Create the Validation Gateway
Write a Python REST API (you may use `Flask` or the standard library's `http.server`) and save it to `/home/user/gateway.py`. The server must meet the following specifications:
1. Listen precisely on `127.0.0.1:9090`.
2. Implement a single endpoint: `POST /build`.
3. The endpoint must accept a JSON payload with a `"source"` key containing raw x86_64 assembly code. Example: `{"source": "global _start\n_start:\nmov rax, 1\n"}`
4. The application must write this assembly code to a temporary file and use `nasm` to compile it into a 64-bit ELF object file (`nasm -f elf64`).
5. If the assembly compilation fails, return an HTTP 400 response with a JSON payload: `{"error": "compilation failed"}`.
6. If the compilation succeeds, read the raw bytes of the generated object file.
7. Compute the SHA-256 hash of the compiled binary bytes concatenated directly with the `AUTH_SEED` extracted from the image (encoded as UTF-8). 
   * Hash Input = `binary_bytes + seed_string_bytes`
8. Return an HTTP 200 response with the JSON payload: `{"hash": "<sha256_hex_digest>"}`.

Step 3: Run the Service
Ensure `nasm` and `tesseract-ocr` are installed on the system (using `sudo apt-get` if necessary, assuming passwordless sudo is available, or use local equivalents). Start your Python server in the background so that it listens continuously on `127.0.0.1:9090`. Leave the server running.

Requirements:
- Ensure the server is robust enough to handle multiple sequential requests.
- Ensure temporary files created during the compilation step are stored securely and uniquely (e.g., using the `tempfile` module) to avoid race conditions.