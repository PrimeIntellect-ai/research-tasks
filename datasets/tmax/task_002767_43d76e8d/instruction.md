You are a log analyst investigating a recent anomaly in our time-series metrics pipeline. 

We use a custom Rust-based tool, vendored at `/app/log-processor`, to clean and reshape our daily metric logs. It acts as a standard Unix filter, reading CSV data from `stdin` and writing the processed CSV to `stdout`.

Recently, we discovered that the tool silently drops log entries if the `message` field contains an embedded newline. We suspect the developer who originally vendored the code applied a quick hack that manually splits the input by `\n` before feeding it to the CSV parser, completely breaking RFC 4180 compliance.

Your task is to fix the Rust project in `/app/log-processor`.

The pipeline's expected behavior is:
1. **Input Format:** Read a CSV from `stdin` containing the following columns: `timestamp, ip, message, cpu_temp, gpu_temp`. The data is UTF-8 encoded and may contain emojis and embedded newlines in the `message` column.
2. **Data Masking:** Anonymize the `ip` address by replacing the final octet with `XXX` (e.g., `192.168.1.50` becomes `192.168.1.XXX`).
3. **Wide-to-Long Reshaping:** Convert the wide format metrics (`cpu_temp`, `gpu_temp`) into a long format. Each input row should produce up to two output rows. The output CSV must have the columns: `timestamp, ip, message, sensor_type, temperature`. `sensor_type` should be either `cpu` or `gpu`.
4. **Imputation:** If a temperature value is missing (empty string) in the input, impute it by carrying forward the *last seen valid temperature* for that specific sensor type. If the very first reading for a sensor is missing, output `0.0` for that row. 

Build your fixed version in release mode. The final executable must be located at `/app/log-processor/target/release/log-processor`. Our automated testing suite will feed it thousands of edge-case CSVs via `stdin` to ensure bit-exact equivalence with our reference implementation.