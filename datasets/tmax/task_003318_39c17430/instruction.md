You are a DevOps engineer investigating a crash in a telemetry processing service written in Rust. The service calculates the sum of squares for a sliding window of sensor readings. Recently, the service panicked and crashed in production. To make matters worse, a junior developer accidentally ran a destructive command that deleted the `src/main.rs` file.

Your tasks are:
1. **Recover the source code**: The junior developer left a hidden backup file of the source code somewhere in the `/home/user/telemetry_app/src/` directory. Find it and restore it to `/home/user/telemetry_app/src/main.rs`.
2. **Analyze the crash**: A crash log is available at `/home/user/telemetry_app/crash.log`. Use it to understand why the application panicked. 
3. **Fix the mathematical and logic bugs**: 
   - The original code has an integer overflow bug causing the crash. Fix the formula implementation and data types so it can handle large telemetry values without overflowing.
   - The original code has boundary condition errors. It was supposed to calculate the sum of squares for a sliding window of exactly **5** elements. Fix the off-by-one errors in the loops so that the sliding window processes exactly 5 elements per window and computes a result for every valid window in the sequence (e.g., a sequence of 10 elements should produce exactly 6 window results).
4. **Generate the corrected output**: Compile and run your fixed Rust program. It must read the raw data from `/home/user/telemetry_app/input_logs.txt` and output the correct sliding window results to `/home/user/telemetry_app/corrected_metrics.txt`. Each line in the output file should contain exactly one computed integer value.

Ensure that `/home/user/telemetry_app/corrected_metrics.txt` is created with the correct values.