You are a DevOps engineer investigating a critical failure in a log processing pipeline. The Rust-based log processing service crashed and accidentally deleted the raw log file it was currently processing. 

Fortunately, we have a partial dump of the filesystem block device at `/home/user/disk_image.bin`. 

Your objectives are:

1. **Recover the deleted logs:** Inspect `/home/user/disk_image.bin` and extract the lost log entries. The log entries are ASCII strings scattered through the binary garbage. Every valid log line is prefixed with the string `LOG_ENTRY: ` followed by a JSON object. 
   Extract *only* the JSON objects (strip the `LOG_ENTRY: ` prefix) and save them, one per line, to `/home/user/recovered_logs.jsonl`. Ensure they are valid JSON strings.

2. **Debug the Log Processor:** The source code for the log processor is located in `/home/user/log_processor`. It has two known bugs:
   * **Boundary/Off-by-One Error:** The program currently panics due to an out-of-bounds index error when processing the log vectors. Find and fix this off-by-one error.
   * **Floating-Point Precision Loss:** The program computes the sum of the `sensor_val` fields. Because it accumulates these values using 32-bit floats (`f32`), it suffers from precision loss on large datasets, resulting in an inaccurate final sum. Upgrade the accumulation logic to use 64-bit floats (`f64`) to guarantee exact precision.

3. **Generate the Metrics:**
   Once fixed, build and run the log processor using Cargo. It takes two arguments: the input log file and the output metrics file.
   Command format: `cargo run -- <input_file> <output_file>`
   
   Run the processor on your recovered logs:
   `cargo run -- /home/user/recovered_logs.jsonl /home/user/metrics.json`

Ensure `/home/user/metrics.json` is successfully created with the correct, precise total sensor value and without crashing.