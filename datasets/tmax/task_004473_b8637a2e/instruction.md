You are a build engineer managing an internal artifact caching system. The system consists of a custom, high-performance local caching server written in Rust and a suite of benchmarking tools. 

Currently, the Rust caching server is failing to compile due to a borrow checker error. The server uses a custom data structure to store artifacts in memory, but there is an ownership issue in how the URL routing parameters are parsed and stored in the cache.

Your tasks are:

1. **Fix the Rust Server**: 
   Navigate to `/home/user/artifact_server`. You will find a Rust project. The `src/main.rs` file contains a custom `ArtifactStore` struct and a simple TCP HTTP parser. 
   - Fix the ownership and borrow checker issues so the project compiles successfully using `cargo build --release`. 
   - Do not change the core logic, just fix the types/lifetimes/ownership. 
   - The server must listen on `127.0.0.1:8080`. Run it in the background (`cargo run --release &`).

2. **Benchmarking and Numerical Algorithm**:
   Write a Python 3 script at `/home/user/benchmark.py`.
   - The script must send 500 HTTP GET requests to the Rust server at the URL `http://127.0.0.1:8080/artifact/v2/linux?id=<N>` where `<N>` goes from 1 to 500.
   - Record the round-trip latency for each request in milliseconds.
   - Implement a custom numerical algorithm in Python (using ONLY the standard library, do NOT use `numpy` or `statistics`) to calculate the 95th percentile (p95) latency. Calculate it by sorting the latencies and picking the value at the `int(0.95 * N)` index.
   - The script must write the final p95 latency value as a floating point number (rounded to 2 decimal places) to the file `/home/user/p95_result.txt`.

Ensure your Rust server is running and the `p95_result.txt` file is generated correctly.