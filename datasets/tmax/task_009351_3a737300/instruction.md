You are a mobile build engineer maintaining a local CI pipeline for a data processing application. We have a small backend service that wraps a high-performance C library (`libencoder.so`) used to encode strings before they are sent to our mobile clients.

Currently, the pipeline is broken and lacks some required API features. Your workspace is located at `/home/user/mobile_pipeline`.

Here is what you need to do:

1. **Fix the Build System (Shared Library/ABI Management):**
   There is a C source file `encoder.c` and a `Makefile` in `/home/user/mobile_pipeline/c_src/`. 
   Running `make` currently fails to produce a valid shared library or throws a linking error. Modify the `Makefile` so that it correctly compiles `encoder.c` into a shared library named `libencoder.so` (ensure position-independent code and shared flags are used). Copy the resulting `libencoder.so` to `/home/user/mobile_pipeline/`.

2. **Enhance the API (Request Validation & Rate Limiting):**
   There is a skeleton Python app at `/home/user/mobile_pipeline/app.py` written in Flask. It loads `libencoder.so` via `ctypes` and exposes a `POST /encode` endpoint expecting JSON: `{"text": "your_string"}`.
   You must update `app.py` to:
   - **Request Validation:** Ensure the `text` field exists, is a valid string, is strictly less than 50 characters, and contains only ASCII characters. If validation fails, return a `400 Bad Request` status code.
   - **Rate Limiting:** Implement rate limiting on the `/encode` endpoint to allow a maximum of 5 requests per minute per IP. You may use the `Flask-Limiter` package (install it via pip if needed). If the limit is exceeded, return a `429 Too Many Requests` status code.
   - Properly decode the C byte response into a standard Python string before returning it as JSON: `{"encoded": "..."}`.

3. **Create the CI Pipeline Script:**
   Write a bash script at `/home/user/mobile_pipeline/ci_run.sh` that automates the build and integration test. The script must:
   - Navigate to `c_src`, clean, and build the shared library.
   - Move `libencoder.so` to `/home/user/mobile_pipeline/`.
   - Start the Flask app (`app.py`) in the background on port `8080`.
   - Wait for the server to be ready.
   - Use `curl` to send exactly 6 valid `POST` requests sequentially to `http://localhost:8080/encode` with the payload `{"text": "test_string"}`.
   - Extract **only** the HTTP status code (e.g., `200`, `429`) for each of the 6 requests and append each code on a new line to `/home/user/mobile_pipeline/test_results.log`.
   - Shut down the background Flask server cleanly and exit.

Ensure your `ci_run.sh` script has executable permissions. When we test your solution, we will simply execute `/home/user/mobile_pipeline/ci_run.sh` and inspect the `test_results.log` file and your code.