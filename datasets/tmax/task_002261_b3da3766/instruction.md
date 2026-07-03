You are an integration developer building a mock API for testing a data processing pipeline. The pipeline uses a custom error-correcting checksum implemented in C, and you need to expose this functionality over a Python-based HTTP API. The API will be protected by an authentication token provided in an image format.

Perform the following steps:

1. **Extract Authentication Token**: There is an image located at `/app/reference_code.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. The extracted text (with any leading/trailing whitespace removed) will serve as your authentication token.

2. **Compile the C Library**: You have been provided with a C source file at `/app/ecc.c` containing a function `uint32_t compute_ecc(const char* data, int length)`. Compile this file into a shared library named `/app/libecc.so`.

3. **Develop the API Service**: Create a Python HTTP server (you may use Flask, FastAPI, or the standard `http.server`) that listens on `127.0.0.1:9090`.
   - The server must expose a `POST /process` endpoint.
   - **Authentication**: The endpoint must check for the `Authorization: Bearer <token>` header. If the token does not perfectly match the text extracted from the image, the server must return an HTTP 401 Unauthorized status.
   - **Data Processing**: If authenticated, the endpoint should expect a JSON payload in the format `{"data": "<string_to_process>"}`.
   - **FFI Integration**: Use Python's `ctypes` module to load `/app/libecc.so` and pass the received string to the `compute_ecc` function.
   - **Response**: Return an HTTP 200 OK status with a JSON response in the format: `{"status": "ok", "checksum": <integer_result>}`.

4. Keep the server running in the background or foreground so that integration tests can be executed against it.

Make sure you install any required Python packages (like `flask` or `fastapi`) using pip if you choose to use them.