You are an engineer tasked with debugging and fixing a Rust service located in `/home/user/stats_service`. This service is designed to read a large dataset of integers from `/home/user/data.csv`, calculate the mean and the population variance of the numbers, and print the results.

However, the service currently has several issues:
1. **Build Failure**: The project currently fails to compile due to a dependency conflict and a few type mismatch errors in `src/main.rs`.
2. **Statistical Anomaly**: Once compiled, the variance calculated is completely wrong (often negative). You must identify and fix the mathematical bug causing this.
3. **Memory Leak / Inefficiency**: The service is designed to be a long-running streaming processor, but it currently loads all data into memory, causing massive memory spikes. You must modify the code to process the CSV in a streaming fashion, calculating the mean and variance incrementally without storing all the numbers in memory.

Your task:
1. Fix the dependency issues in `Cargo.toml` so the project builds successfully.
2. Fix the mathematical and memory issues in `src/main.rs`. Ensure you use a streaming algorithm for the mean and variance (e.g., Welford's algorithm or simply accumulating `sum` and `sum_sq` using appropriate types that won't overflow).
3. Run the fixed service to process `/home/user/data.csv`.
4. Write the final computed variance (as a floating-point number, rounded to 2 decimal places) to a file named `/home/user/result.txt`.

Ensure your final code compiles cleanly with `cargo build`.