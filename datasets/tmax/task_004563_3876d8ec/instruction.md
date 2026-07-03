You are tasked with fixing a polyglot system containing C, Rust, and Python code, and deploying the final Python web service.

Here is the current state of the system:
1. **Configuration Image:** There is an image at `/app/server_config.png` that contains critical configuration details: the server port, the API key, and the target schema migration version. Use an OCR tool like `tesseract` to read it.
2. **C Dependency:** In `/home/user/clib`, there is a C library used for core calculations. Its `Makefile` is broken, and `math_ops.c` contains a logical error in the `add` function (it subtracts instead of adding). Fix the C code and the Makefile so it produces a static library `libmathops.a`.
3. **Rust Project:** In `/home/user/rust_svc`, there is a multi-file Rust CLI project that depends on the C library. It is currently failing to compile due to a missing `unsafe` block when calling the C FFI, and a type mismatch. Fix the Rust code so that `cargo build --release` successfully produces the binary at `/home/user/rust_svc/target/release/rust_svc`. The binary takes two integers as arguments and prints their sum.
4. **Schema Migration:** In `/home/user/schema/`, there are multiple schema diff files (`v1.sql`, `v2.sql`, `v3.sql`). You need to write a Python script that concatenates these files in sequential sorted order up to the target migration version specified in the image, and applies them to an SQLite database at `/home/user/app.db`.
5. **Python API Server:** Write a Python HTTP service (e.g., using Flask or FastAPI) in `/home/user/server.py` that:
   - Listens on the port specified in `/app/server_config.png`.
   - Exposes a `POST /compute` endpoint.
   - Requires an `X-API-Key` header matching the API key from the image.
   - Accepts a JSON payload like `{"a": 10, "b": 15}`.
   - Calls the compiled Rust binary with these arguments.
   - Returns the JSON response `{"result": 25}` based on the Rust binary's output.

Bring up the Python server in the background so it is ready to accept requests. Ensure all bugs in the C and Rust code are fixed.