You are a data engineer troubleshooting an ETL pipeline stage. We have a Rust project located at `/home/user/pipeline` that processes sensor data. 

Currently, the pipeline has a critical bug: it silently drops rows if the `location_notes` field contains embedded newlines, because the original author used standard line-by-line string splitting (`BufRead::lines`) to parse the CSV.

Your task is to fix the Rust program (`/home/user/pipeline/src/main.rs`) to accomplish the following:
1. Robustly parse the CSV file `/home/user/pipeline/input.csv` to correctly handle embedded newlines in the `location_notes` column. The `csv` crate is already included in the `Cargo.toml`.
2. Compute the Euclidean distance of the `(x, y)` coordinates from the origin `(0.0, 0.0)`.
3. Act as a validation quality gate: silently drop any rows where this computed Euclidean distance is strictly greater than `50.0`.
4. Output the valid records to `/home/user/pipeline/cleaned.csv` with a header row. The output CSV must contain exactly two columns: `timestamp` and `distance`.
5. The `distance` values must be rounded to exactly 2 decimal places (e.g., `22.36`).

Once you have fixed the code, compile and run it to produce the `cleaned.csv` file. 

Files provided:
- `/home/user/pipeline/Cargo.toml`
- `/home/user/pipeline/src/main.rs` (Broken implementation)
- `/home/user/pipeline/input.csv` (Raw data)