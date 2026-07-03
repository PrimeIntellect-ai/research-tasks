You have recently inherited an unfamiliar codebase for a sensor processing pipeline written in Rust. The application reads batches of sensor readings from a CSV file, calculates the population variance for each batch, and prints the result to standard output. 

However, the pipeline is crashing in production. The system logs show that the Rust program panics with an assertion failure: `"Variance cannot be negative!"`. This statistical anomaly only manifests with specific input sequences due to a floating-point precision issue in the current variance calculation algorithm.

Your task is to:
1. Navigate to the Rust project located at `/home/user/anomaly_detector`.
2. Analyze the traceback and the code in `src/main.rs` to understand why the floating-point calculation is losing precision and resulting in a negative variance (catastrophic cancellation).
3. Repair the floating-point calculation by replacing the naive variance algorithm with a numerically stable algorithm (e.g., a two-pass algorithm or Welford's online algorithm) to compute the population variance.
4. Compile the fixed program and run it against the production data located at `/home/user/sensor_data.csv`.
5. Redirect the standard output of your successful run to `/home/user/fixed_output.txt`.

The format of `/home/user/fixed_output.txt` must be exactly one floating-point number per line, corresponding to the variance of each line in the input CSV file. You do not need to format the floats to a specific number of decimal places, but the values must be numerically correct and mathematically valid (non-negative).