You are a developer organizing project files into a proprietary binary archive format. We have an existing verification tool, but we need a web service that dynamically creates these archives. 

Your task is to build a multi-language solution:
1. Write the serialization logic in C. It must be compiled into a shared library (`libpack.so`) using a `Makefile` that you create.
2. Write a Python HTTP server listening on `127.0.0.1:8888` that handles the web requests, uses the C library for serialization, and verifies the output.

**Archive Format Specification:**
- Magic bytes: `ARCH` (4 bytes, ASCII)
- Project ID: 4 bytes (unsigned 32-bit int, little-endian)
- Number of files: 2 bytes (unsigned 16-bit int, little-endian)
- For each file in sequence:
  - Name length: 2 bytes (unsigned 16-bit int, little-endian)
  - Name: ASCII string (exact length specified above, no null-terminator)
  - Content length: 4 bytes (unsigned 32-bit int, little-endian)
  - Content: Raw bytes of the file content

**Web Service Requirements:**
- Protocol: HTTP
- Listen Address: `127.0.0.1:8888`
- Endpoint: `POST /pack`
- Content-Type: `application/json`
- Request Payload Example:
  ```json
  {
    "project_id": 1024,
    "files": [
      {"name": "src/main.c", "content": "int main() {}"},
      {"name": "README.md", "content": "Hello World"}
    ]
  }
  ```
- **Processing Logic**:
  1. The Python server parses the JSON.
  2. It passes the data to your `libpack.so` C library to serialize into the custom binary format in memory.
  3. The Python server writes this binary output to a temporary file (e.g., `/tmp/temp_archive.bin`).
  4. The Python server executes the provided stripped binary `/app/validator` with the temporary file path as its only argument (e.g., `/app/validator /tmp/temp_archive.bin`).
  5. If the validator exits with code 0, return the binary archive in the HTTP response body with status `200 OK` and `Content-Type: application/octet-stream`.
  6. If the validator fails (non-zero exit code), return status `500 Internal Server Error`.

**Constraints:**
- The C code must be compiled via a `Makefile` into `libpack.so`.
- Use standard Python 3 libraries (e.g., `http.server`, `ctypes`, `json`, `subprocess`). No external frameworks like Flask or FastAPI are required or provided.
- You must start the Python server in the background and leave it running so it can be tested. Ensure it binds successfully to `127.0.0.1:8888`.