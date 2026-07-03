You are a platform engineer responsible for maintaining our CI/CD pipelines. We recently started migrating our internal log parsing tools to Rust for performance, exposing them to Python via PyO3. 

Unfortunately, the offline vendored package for the new parser, located at `/app/vendored/ci-log-decoder`, is broken. Since the build servers run in an air-gapped environment (no internet access), you must fix the code locally, build it, and deploy it as a standalone parsing service.

**Task Requirements:**

1. **Fix the Build Configuration:** 
   The package's `pyproject.toml` was accidentally overwritten by a generic Python boilerplate. It currently fails to build the Rust extension. You need to correct the build backend configuration so that it correctly builds the PyO3 Rust extension using `maturin`.

2. **Fix the Rust Parser:**
   The Rust code in `/app/vendored/ci-log-decoder/src/lib.rs` implements a state machine to decode a custom log encoding. However, it currently fails to compile due to a Rust ownership and borrow checker error involving string slicing and state transitions. Fix the borrow checker error without changing the intended logic or parser behavior.

3. **Install the Package:**
   Once fixed, build and install the Python package into the local environment (e.g., using `pip install .` or `maturin develop` inside the package directory).

4. **Create the Parsing Service:**
   Write a Python HTTP server script at `/app/server.py` that imports the newly installed `ci_log_decoder` module.
   - The server must listen on `127.0.0.1:8181`.
   - It must expose a single endpoint: `POST /parse`.
   - The endpoint will receive raw encoded binary data in the request body.
   - It must pass the binary data (as bytes) to the Rust parser function: `ci_log_decoder.decode_log(data)`.
   - It must return the parsed output as a JSON response with a `200 OK` status code and `Content-Type: application/json`.

**Log Encoding Details (for your reference):**
The Rust state machine parses logs where messages are prefixed by a start byte (`0x02`), followed by the message length (1 byte), followed by the utf-8 message data, and ending with an end byte (`0x03`). 

Keep the server running in the foreground once you start it so the automated tests can verify it.