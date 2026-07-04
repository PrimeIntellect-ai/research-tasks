You are a web developer tasked with building a high-performance, secure token masking API. Your company has a legacy C-based cryptography library that applies a proprietary mask to sensitive tokens. You need to fix the library's build system, wrap it in a secure Rust web server, and benchmark it using Go concurrency patterns to ensure it can handle burst traffic.

All work should be done in `/home/user/workspace`.

**Phase 1: Fix the Legacy C Library**
In `/home/user/workspace/legacy_crypto/`, there is a broken `Makefile`, `crypto.c`, and `crypto.h`. 
1. The `Makefile` is supposed to compile a shared library named `libcrypto_mask.so`, but it currently fails to build or link correctly. Fix the `Makefile` so that running `make` successfully produces `libcrypto_mask.so`.

**Phase 2: Build the Rust API**
1. Create a new Rust Cargo project (executable) in `/home/user/workspace/rust_api/`.
2. The Rust application must run an HTTP server on `127.0.0.1:8080` (you may use `axum` or `actix-web`, along with `tokio` and `serde`).
3. Create a `POST /secure-token` endpoint that accepts a JSON payload in the format `{"token": "secret123"}`.
4. Using Rust's FFI, the endpoint must call the C function `void apply_mask(const char* input, char* output)` from `libcrypto_mask.so` to mask the token. Assume the output buffer needs to be at least as large as the input string + 1.
5. The endpoint must return a JSON response in the format `{"masked": "<result_from_c>"}`.
6. Write at least one standard Rust unit test (`#[test]`) in your codebase that directly tests the FFI call to `apply_mask`.

**Phase 3: Benchmarking with Go**
1. Write a Go script at `/home/user/workspace/bench.go`.
2. The Go script must use Go concurrency patterns (goroutines and channels) to send exactly 500 concurrent POST requests to your Rust server's `/secure-token` endpoint. 
3. The payload for each request should be `{"token": "bench_test"}`.
4. The Go script must aggregate the results and write the total number of HTTP 200 OK responses to a file at `/home/user/workspace/bench_report.txt` in the exact format: `Success: <number>`.

**Requirements & Deliverables:**
- Ensure your Rust server is running in the background when you complete the task.
- Ensure your `bench_report.txt` is generated.
- Your FFI integration must be memory-safe (preventing buffer overflows given by the C library). 
- Leave the Rust server running on port 8080.