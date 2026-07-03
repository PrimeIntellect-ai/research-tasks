You are tasked with building a lightweight Web Security anti-spam proxy. You must fix a vendored native library, implement a numerical rate-limiting algorithm, and expose an HTTP API using Python.

**Part 1: Fix the Vendored Library**
There is a vendored Rust library located at `/app/pow_shield` which performs high-performance Proof-of-Work (PoW) validation. 
1. The project has a `Makefile` that builds the Rust library and is supposed to output a shared object (`libpow_shield.so`). However, there is a build/linking configuration error preventing the shared library from being generated properly.
2. The Rust source code in `src/lib.rs` contains an ownership/borrow checker error related to a vector and slice used during the validation routine.
You must debug and fix both the build configuration and the borrow checker error, then run `make` so that `libpow_shield.so` is successfully produced in `/app/pow_shield/`.

**Part 2: Build the Python Security Proxy**
Create a Python web server at `/home/user/proxy.py`.
1. **Package Management**: Set up a virtual environment in `/home/user/venv` and install `Flask`.
2. **Integration**: Use Python's `ctypes` to load `/app/pow_shield/libpow_shield.so`. The Rust function exposed is:
   `bool verify_pow(const uint8_t* data, size_t len, uint64_t nonce, uint32_t target);`
3. **HTTP Server**: Implement a Flask server listening on `127.0.0.1:8000`. 
4. **Endpoint**: Provide a `POST /submit` endpoint that accepts JSON: `{"data": "<string>", "nonce": <int>, "target": <int>}`.
5. **Validation**: Pass the `data` (as UTF-8 bytes), `nonce`, and `target` to the Rust `verify_pow` function. If it returns `false`, immediately return an HTTP `403` status with JSON `{"error": "Invalid PoW"}`.
6. **Numerical Rate Limiting**: To prevent abuse, implement an Exponential Moving Average (EMA) rate limiter in Python for the endpoint (globally, across all requests).
   - Initialize the `EMA` to `500.0` (representing milliseconds).
   - For every request *after* the first one, calculate the time difference in milliseconds (`diff_ms`) since the last received request.
   - Update the EMA using the formula: `EMA = (diff_ms * 0.3) + (previous_EMA * 0.7)`.
   - After updating, if `EMA < 100.0`, reject the request by returning HTTP `429` with JSON `{"error": "Too Fast"}`.
   - If the PoW is valid and the request is not rate-limited, return HTTP `200` with JSON `{"status": "Accepted"}`.

Start the web server in the background or use a terminal multiplexer so it remains running on port `8000`.