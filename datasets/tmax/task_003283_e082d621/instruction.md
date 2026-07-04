I am a web developer building a high-performance metrics aggregator for our legacy C-based web server. I want to replace the current latency tracking module with a more memory-safe and faster Rust implementation using FFI, while keeping the rest of the C architecture intact.

Your task is to write a Rust library that implements a custom Ring Buffer (circular queue) to calculate a moving average of response times, exposed via C ABI.

1. Create a Rust file at `/home/user/metrics.rs`.
2. Implement a global, thread-safe Ring Buffer data structure to store `f64` latency values.
3. Expose exactly two C-compatible FFI functions:
   - `void init_metrics(size_t capacity)`: Initializes or resets the global ring buffer to hold up to `capacity` items.
   - `double record_and_average(double latency)`: Inserts the new latency into the ring buffer (overwriting the oldest value if full) and returns the arithmetic mean of all current items in the buffer.
4. Compile the Rust code into a dynamic library named `libmetrics.so` in `/home/user/` (ensure it can be linked by a C compiler).
5. I have already placed a C benchmarking program at `/home/user/bench.c`. It depends on your library. Compile this C file, linking it against your `libmetrics.so`, to an executable named `/home/user/bench_run`.
6. Run `/home/user/bench_run` and redirect its standard output to `/home/user/bench_output.txt`.

Requirements:
- Do not use any external Rust crates (only `std`).
- The ring buffer must correctly maintain the moving average (e.g., if capacity is 3, inserting 10.0, 20.0, 30.0, 40.0 should result in averages 10.0, 15.0, 20.0, and then 30.0 since the buffer holds [40.0, 20.0, 30.0]).
- Ensure the dynamic library is correctly located and `LD_LIBRARY_PATH` is set if necessary when running the executable.