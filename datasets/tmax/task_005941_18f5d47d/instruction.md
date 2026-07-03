You are an automation specialist tasked with building a robust data processing pipeline. We receive daily batches of sensor data in JSON-lines (JSONL) format. The files can be very large, so they must be streamed line-by-line rather than loaded entirely into memory. 

Furthermore, our legacy sensors occasionally emit malformed JSON containing broken unicode escape sequences—specifically, they output the literal string `\u001 ` (backslash, 'u', '0', '0', '1', space) instead of a valid four-hex-digit sequence. 

Your task is to create a Rust application that processes this data, normalizes it, and schedule it to run automatically.

Perform the following steps:

1. Create a new Rust project named `log_processor` in `/home/user/log_processor`.
2. Write a Rust program that reads `/home/user/data/raw_logs.jsonl` line-by-line using a buffered reader.
3. For each line, perform the following operations:
   - **Sanitize**: Replace any literal occurrences of `\u001 ` with `\u0001 ` before parsing.
   - **Parse**: Parse the corrected line as a JSON object.
   - **Normalize**: The JSON object contains a `temp_f` field (a floating-point number representing Fahrenheit). Calculate the Celsius equivalent using the formula `(temp_f - 32.0) * 5.0 / 9.0`. 
   - Round the resulting Celsius value to exactly 2 decimal places.
   - Remove the `temp_f` field and add the calculated value as a new field named `temp_c` (represented as a float).
   - Keep all other fields intact.
   - **Output**: Serialize the normalized object back to a JSON string and write it as a new line to `/home/user/data/normalized_logs.jsonl` using a buffered writer.
4. Build the Rust project in release mode.
5. Create a shell script at `/home/user/run_pipeline.sh` that runs your compiled Rust binary (`/home/user/log_processor/target/release/log_processor`). Make sure the script is executable.
6. Create a cron schedule file at `/home/user/crontab.txt` that schedules `/home/user/run_pipeline.sh` to run every day at exactly 02:30 AM.
7. Install the cron job using `crontab /home/user/crontab.txt`.
8. Execute `/home/user/run_pipeline.sh` manually once to generate the output file.

Constraints:
- You must use Rust as the primary language for the data processing application.
- The Rust application must stream the data (e.g., using `std::io::BufReader` and `std::io::BufWriter`) rather than reading the whole file into a single string.
- You may use popular crates like `serde` and `serde_json`.