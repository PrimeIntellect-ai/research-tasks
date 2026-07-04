You are an automation specialist tasked with building a robust data processing pipeline for IoT sensor logs.

Your objective is to create a Rust-based CLI tool that performs extraction, anonymization, imputation, and reshaping of incoming log data, and then deploy it as a scheduled job.

### Part 1: Fix the Vendored Library
We have a local Rust library located at `/app/anonymizer_lib` which is supposed to handle PII masking (names and IPs). However, the previous developer left it in a broken state (it fails to compile). 
1. Identify and fix the deliberate perturbation in `/app/anonymizer_lib/Cargo.toml` or source code so that it compiles.

### Part 2: Build the Data Processor
Create a new Rust binary project at `/home/user/processor`. It must depend on the local `/app/anonymizer_lib` crate.
The CLI tool must read lines of text from `stdin` and output transformed CSV lines to `stdout`.

**Input Format:**
Each line from standard input will be a semicolon-separated string:
`ID:<integer>;USER:<string>;IP:<ipv4>;S1:<float|NA>;S2:<float|NA>;S3:<float|NA>`
Example: `ID:402;USER:alice;IP:192.168.1.5;S1:10.5;S2:NA;S3:12.5`

**Processing Rules:**
1. **Extraction:** Parse the fields.
2. **Masking:** Use the fixed `anonymizer_lib` to mask the `USER` (should become `***`) and `IP` (should become `0.0.0.0`).
3. **Imputation:** Sensor values (S1, S2, S3) can be floats or the string "NA".
   - If exactly one sensor is "NA", its value becomes the average of the other two valid sensors.
   - If exactly two sensors are "NA", both take the value of the single valid sensor.
   - If all three sensors are "NA", all of them become `0.0`.
4. **Reshaping (Wide to Long):** For each input line, output exactly three lines to `stdout` in CSV format (one for each sensor), in the order S1, S2, S3.
   Format: `<ID>,<MASKED_USER>,<MASKED_IP>,<SENSOR_NAME>,<VALUE>`
   *Note: Format the `<VALUE>` to exactly 2 decimal places (e.g., `11.50`).*

Example Output for the above input:
```csv
402,***,0.0.0.0,S1,10.50
402,***,0.0.0.0,S2,11.50
402,***,0.0.0.0,S3,12.50
```

Build your tool in release mode (`cargo build --release`). The executable must be at `/home/user/processor/target/release/processor`.

### Part 3: Scheduling
Create a bash script at `/home/user/run_pipeline.sh` that cats `/tmp/input.log` into your processor and redirects the output to `/tmp/output.csv`. Make it executable.
Then, create a cron job file at `/etc/cron.d/sensor_processor` that runs `/home/user/run_pipeline.sh` as `user` every 5 minutes.