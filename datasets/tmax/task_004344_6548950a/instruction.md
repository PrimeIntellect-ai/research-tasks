You are an ML Engineer preparing and benchmarking a data ingestion pipeline. You have a raw binary file containing a large 1D feature tensor. You need to write a Rust program to read this data, perform a foundational linear algebra operation, and benchmark its execution time.

Here are the requirements:
1. There is a raw binary file located at `/home/user/data/features.bin`. It contains exactly 1,000,000 `f32` (32-bit floating point) values stored in little-endian format.
2. Write a Rust program (you can create a Cargo project in `/home/user/feature_processor` or just use a single `main.rs` file compiled with `rustc`).
3. The Rust program must:
   - Read all the `f32` values from `/home/user/data/features.bin` into memory.
   - Start a high-precision timer.
   - Compute the L2 norm (Euclidean norm) of this entire 1,000,000-element vector.
   - Stop the timer.
4. The program must then write the result to a JSON file located at `/home/user/metrics.json`.
   The JSON file must have exactly this structure:
   ```json
   {
     "l2_norm": 123.45,
     "compute_time_us": 456
   }
   ```
   - `l2_norm` must be a float representing the computed L2 norm.
   - `compute_time_us` must be an integer representing the elapsed time of the computation in microseconds (do NOT include the file I/O time in this benchmark).

Compile and run your Rust program so that the `/home/user/metrics.json` file is successfully created with the correct computed results.