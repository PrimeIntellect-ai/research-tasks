You are an integration developer responsible for finalizing a Rust library used for a WebSocket-based data processing API. The project is located at `/home/user/ws_encoder_api`. It wraps a legacy C library for custom data encoding (hexadecimal formatting) and includes rate-limiting logic to protect the WebSocket endpoints. 

However, the repository is currently broken and failing tests due to several issues:

1. **Broken Build System:** The `build.rs` file is completely empty. It needs to compile the C code located at `c_src/hex_encoder.c` and link it as a static library named `hex_encoder`. You must use the `cc` crate in `build.rs` to achieve this.
2. **C Memory Safety (Undefined Behavior):** The C function `char* encode_hex(const unsigned char* input, size_t len)` in `c_src/hex_encoder.c` has a memory allocation bug. It allocates exactly `len * 2` bytes for the hex string, which forgets the null terminator, leading to undefined behavior and random test crashes. Fix the C code to safely allocate and null-terminate the string.
3. **Rate Limiting & Validation Implementation:** The Rust file `src/rate_limit.rs` contains a stubbed `RateLimiter` struct. You must implement the `check_and_record(&mut self, client_id: u32) -> bool` method. It should implement a simple sliding window or token bucket that allows a maximum of 3 requests per client. For this task, a simple counter per `client_id` that rejects requests if the count exceeds 3 is sufficient, as the tests mock a single second window.
4. **Integration Testing:** Once you have fixed the build script, the C memory bug, and the rate limiter, run `cargo test`. 

To prove successful completion of the task, redirect the standard output and standard error of your final successful `cargo test` run to `/home/user/test_results.log`. 

Ensure that `/home/user/test_results.log` contains the passing results for all integration and unit tests before concluding.