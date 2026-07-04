You are tasked with building a robust data processing filter for a configuration management system. Our servers emit configuration telemetry logs that track numeric configuration changes (like cache sizes, thread limits) over time. 

We have a legacy, closed-source analysis engine located at `/app/telemetry_oracle` (a stripped binary). This oracle reads processed telemetry from standard input and updates our backend metrics. However, the raw telemetry logs are messy and have recently been targeted by adversarial injection attacks. 

Your objective is to write a Rust command-line tool in `/home/user/config_sanitizer` that reads a raw telemetry CSV file, cleans and sanitizes the data, and prints the processed CSV to standard output.

**Input Format (Raw CSV):**
`timestamp_raw,config_key,value_raw,hash`
- `timestamp_raw`: Mixed formats (e.g., ISO8601 strings or Unix epoch strings).
- `config_key`: The string path of the configuration (e.g., `sys.cache.size`).
- `value_raw`: The numeric value (can be missing/empty).
- `hash`: An MD5 hash of the configuration state.

**Processing Requirements:**
1. **Timestamp Alignment & Parsing**: Parse all timestamps into standard Unix epoch integers (seconds). Round down to the nearest 10-second bucket (e.g., 1622543217 becomes 1622543210).
2. **Hash-Based Deduplication**: Within each 10-second bucket, if multiple rows have the exact same `config_key` and `hash`, keep only the earliest chronological entry (before bucketing). Drop the duplicates.
3. **Interpolation & Imputation**: The system occasionally fails to record `value_raw`. For any missing numeric value, impute it using linear interpolation between the most recent prior valid value and the next valid value for that specific `config_key`. If there is no prior value, default to 0. If there is no subsequent value, carry forward the last known value. Output values as integers (round nearest).
4. **Adversarial Filtering**: The `/app/telemetry_oracle` binary will violently crash if fed malicious data. Your Rust program MUST exit with code `1` immediately (printing nothing more) if it detects any of the following in the input:
   - A `config_key` containing shell metacharacters (e.g., `$`, `|`, `>`, `<`) or directory traversal attempts (`../`).
   - Any interpolated or raw configuration value that evaluates to less than 0 or strictly greater than 10000.

**Output Format (Processed CSV to stdout):**
`epoch_bucketed,config_key,interpolated_value,hash`
(Output must be sorted by `epoch_bucketed` ascending, then `config_key` alphabetical).

**Integration & Testing:**
You can test your binary's output against the oracle by piping your output into it:
`cargo run --release -- /path/to/raw.csv | /app/telemetry_oracle`
The oracle exits `0` if the stream is perfectly formatted and safe.

Create the Rust project, implement the sanitizer, and ensure the compiled binary at `/home/user/config_sanitizer/target/release/config_sanitizer` takes exactly one file path as a CLI argument.