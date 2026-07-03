You are tasked with fixing a multi-file Rust project that currently fails to compile because its custom build system relies on a missing local build-assistance server.

The Rust project is located at `/home/user/rust_proj`. Its `build.rs` script makes concurrent HTTP GET requests to a local server to evaluate complex mathematical expressions at compile-time to generate `config.rs`. Because the server is missing, `cargo build` fails.

Your objective is to write the missing Python server at `/home/user/server.py` and successfully compile the Rust project.

Requirements for `/home/user/server.py`:
1. **URL Routing & Concurrency**: Create an asynchronous Python web server (using `asyncio` and `aiohttp`, or the built-in `asyncio` streams) that listens on `127.0.0.1:8080`. It must handle multiple requests concurrently (mimicking Go's goroutine concurrency model).
2. **Expression Parsing**: Expose an endpoint `GET /evaluate`. It should accept a query parameter `expr` containing a mathematical expression as a string (e.g., `expr=3*(4+5)`). The server must parse and evaluate this expression safely (supporting addition `+`, subtraction `-`, multiplication `*`, and division `/`, along with parentheses). You may use Python's `ast` module.
3. **Performance Benchmarking**: For every request to `/evaluate`, your server must benchmark how long the expression parsing and evaluation takes in microseconds.
4. **Logging**: The server must append the benchmark result to `/home/user/perf.log` in the exact format: `[EXPR] <expr> [RESULT] <result> [TIME_US] <time_in_microseconds>`.
5. **Response**: The HTTP response must be plain text containing just the integer result of the evaluated expression.

Steps to complete:
1. Write the `/home/user/server.py` script.
2. Start the server in the background.
3. Navigate to `/home/user/rust_proj` and run `cargo build`.
4. Ensure the Rust compilation succeeds. The Rust binary will be placed in `/home/user/rust_proj/target/debug/rust_proj`.