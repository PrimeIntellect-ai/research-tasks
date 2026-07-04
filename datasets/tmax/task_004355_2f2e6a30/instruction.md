You are an engineer porting a mathematical evaluation daemon to run inside a minimal container environment.

We have a vendored third-party Rust application located at `/app/math-daemon`. This application is an HTTP-based interpreter for a custom mathematical bytecode. It uses a channel-based worker pool to process evaluations concurrently (similar to Go's goroutine/channel patterns, implemented via Rust's `mpsc`).

Currently, the daemon is failing its property-based tests, and its network configuration is hardcoded in a way that prevents it from receiving external traffic when containerized.

Your task:
1. Navigate to `/app/math-daemon`.
2. Run the tests using `cargo test`. You will notice that a property-based test (using the `proptest` crate) in `src/interpreter.rs` fails. The interpreter panics when encountering a division by zero in the bytecode (Opcode `0x04`). 
3. Fix the bug in `src/interpreter.rs` so that division by zero gracefully returns an error string `"DivisionByZero"` instead of panicking. Ensure all `cargo test` checks pass.
4. Update the HTTP server configuration in `src/main.rs`. It is currently hardcoded to bind to `127.0.0.1:9000`. To work correctly in our minimal container setup, modify it to bind to `0.0.0.0:9000`.
5. Compile and start the service in the background (e.g., `cargo run --release &`). 

Leave the service running on port 9000 so that our automated systems can verify its operation by sending HTTP requests.