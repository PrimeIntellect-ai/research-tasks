You are a data scientist cleaning up experiment tracking logs for inference performance benchmarking. We have a set of CSV files containing benchmark runs, and we need to automatically filter out the "bad" runs (anomalies where the system was underperforming).

Your task is to write a Rust CLI tool that acts as a binary classifier for these log files.

Here is what you need to do:
1. Examine the image located at `/app/config_formula.png`. It contains a handwritten note defining the maximum acceptable threshold for a computed metric. Use OCR (like `tesseract`) to read it.
2. Create a Rust project named `filter_logs` in `/home/user/filter_logs`.
3. The Rust program must accept exactly one argument: the path to a CSV file.
4. The CSV files have headers including `inference_time_ms` (float) and `batch_size` (float).
5. The program should read the CSV, calculate the product of `inference_time_ms` and `batch_size` for each row, and then compute the mathematical average (mean) of these products across all rows in the file.
6. If the calculated mean is strictly greater than the threshold you extracted from the image, the program must exit with status code `1` (rejecting the log).
7. If the mean is less than or equal to the threshold, the program must exit with status code `0` (accepting the log).
8. Build your Rust project in release mode so the executable is available at `/home/user/filter_logs/target/release/filter_logs`.

Note: You can use any external crates you need (like `csv` or `serde`) by adding them to your `Cargo.toml`. Make sure your code cleanly handles the CSV headers. Do not print anything to stdout/stderr in your final binary, just return the correct exit code.