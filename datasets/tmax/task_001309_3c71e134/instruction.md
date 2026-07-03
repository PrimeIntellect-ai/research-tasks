We are in the process of migrating our legacy Python 2 cryptographic math microservice to Python 3. The service offloads heavy mathematical data encoding to a Rust library to meet strict performance benchmarks, but the migration is currently stalled.

You need to step in and complete the migration, fix the build, and bring up the server.

Here is what you need to do:

1. **Recover the Missing Specification:**
   The original spec document was lost, but we found a cropped screenshot of the encoding formula at `/app/legacy_formula.png`. You will need to use OCR (e.g., `tesseract` is installed) to extract the text. The image contains a crucial integer variable assignment: `ENCODING_MULTIPLIER = [number]`. You will need this number for the server logic.

2. **Fix the Rust Performance Library:**
   Our Rust library at `/app/rust_math` was modified by a junior developer to optimize memory usage, but it currently fails to compile due to a classic Rust ownership and borrow checker error. 
   - Fix the `src/lib.rs` file so it compiles successfully.
   - The library must pass its internal benchmark tests (`cargo bench` must succeed).
   - Build the library in release mode (`cargo build --release`) so the Python server can load the `.so` file.

3. **Migrate and Implement the Python Server:**
   The legacy Python 2 server script is located at `/app/server.py`. 
   - Migrate it to Python 3. You will need to fix `str` vs `bytes` encoding issues common in Python 2 to 3 migrations, specifically around base64 encoding and character data processing.
   - The server must listen for HTTP requests on `127.0.0.1:8080`.
   - Implement the `POST /encode` endpoint. 
   - **Authentication:** The endpoint must require an `Authorization` header with the exact value: `Bearer migrate-token-2024`.
   - **Request Format:** JSON body `{"data": "string to encode"}`
   - **Processing Logic:** 
     a. Convert the string to utf-8 bytes.
     b. Call the Rust library's `process_bytes` function via `ctypes`. Pass the bytes, the length, and the `ENCODING_MULTIPLIER` you recovered from the image.
     c. Base64-encode the resulting bytes returned by the Rust function.
   - **Response Format:** JSON body `{"result": "base64_encoded_string"}`

4. **Test Fixtures & Setup:**
   Before running the server, you must create a mock configuration file at `/app/config.json` containing `{"environment": "production", "version": 3}`. The server should read this on startup (add this to `server.py`).

Once you have fixed the Rust code, migrated the Python code, and created the configuration, start the server as a background process so it continues running. We will run an automated test suite against `127.0.0.1:8080/encode` to verify the mathematical encoding, protocol compliance, and correct handling of Python 3 byte semantics.