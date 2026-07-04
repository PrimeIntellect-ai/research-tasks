You have inherited an unfamiliar Rust codebase for a high-throughput sensor data aggregation system. The previous developer left abruptly, leaving behind a buggy Rust implementation and a stripped legacy compiled binary that we use as the "golden reference".

Your goal is to fix the Rust codebase so that its output exactly matches the legacy binary's output, both in terms of completeness (no dropped records) and numerical precision.

Here is the setup:
1. **The Legacy Binary:** Located at `/app/legacy_calc`. It reads a custom binary file format from standard input and outputs a JSON object to standard output representing the aggregated sums for each sensor.
2. **The Rust Codebase:** Located at `/home/user/sensor_aggregator`. You can build it using `cargo build --release`. The executable will be at `/home/user/sensor_aggregator/target/release/sensor_aggregator`.
3. **The Data Format:** The input consists of concatenated 12-byte binary records. Each record has:
   - `sensor_id`: 4 bytes, Little-Endian unsigned integer (`u32`).
   - `reading`: 8 bytes, Little-Endian IEEE 754 floating-point number (`f64`).
4. **The Issues:**
   - **Concurrency / Race Conditions:** The Rust version reads chunks of the file in parallel, but it is occasionally dropping records or failing to aggregate them properly. The legacy binary always counts every record.
   - **Precision Loss:** The legacy binary maintains high precision, but the Rust codebase has a bug causing floating-point precision loss over millions of records. 
   - **Encoding/Serialization:** The final JSON output of the Rust codebase sometimes misrepresents the exact floating-point sums due to how it serializes the output or deserializes the bytes.

**Your Tasks:**
1. Investigate `/app/legacy_calc` using tools like `xxd`, `strings`, or by feeding it minimized test data to understand its exact behavior.
2. Debug and fix the Rust codebase in `/home/user/sensor_aggregator`. You should use delta debugging principles (creating small test files) to isolate the precision loss and concurrency bugs.
3. Ensure the fixed Rust program reads the binary file path provided as its first command-line argument, and prints the aggregated JSON to standard output. Format the JSON as a flat map of `"sensor_id": sum`, e.g., `{"1": 10.5, "2": -4.2}`.
4. Compile your final fixed version with `cargo build --release`. 

An automated test will run your compiled Rust binary against a large, hidden binary test file and compare its JSON output to the legacy binary. It will compute the Maximum Absolute Error (MAE) across all sensor sums.