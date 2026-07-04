As a data analyst, I need to build a high-performance log analysis tool to extract anomalous IP addresses from a set of remote server logs. 

An HTTP server is already running on `http://127.0.0.1:8123` and is serving three CSV files: `data1.csv`, `data2.csv`, and `data3.csv`.

Your task is to write a Rust program that performs the following:
1. Create a new Rust project called `anomaly_detector` at `/home/user/anomaly_detector`.
2. Fetch the three CSV files from the local server (`http://127.0.0.1:8123/data1.csv`, `http://127.0.0.1:8123/data2.csv`, `http://127.0.0.1:8123/data3.csv`).
3. Parse the CSV files. Each file has a header and three columns: `timestamp`, `server_name`, and `log_message`.
4. Process the downloaded logs in parallel (e.g., using `rayon` or concurrent `tokio` tasks) for maximum throughput.
5. Use a regular expression to search the `log_message` column for critical failure logs. The pattern to match is exactly:
   `E-500: Failed connection from <IP>`
   where `<IP>` must be a valid IPv4 address format (e.g., `192.168.1.1`).
6. Extract all unique IPv4 addresses that appear in this specific error message across all three files.
7. Save the final list of unique IP addresses, sorted alphabetically, as a JSON array of strings to `/home/user/anomalies.json`.

Please write the complete code, build it, and execute it so that the final `/home/user/anomalies.json` file is successfully generated. You may use standard Rust crates (like `reqwest`, `tokio`, `rayon`, `regex`, `csv`, `serde_json`).