You are a data engineer tasked with building an ETL pipeline using a Makefile as a DAG orchestrator and Rust as the primary data processing language.

You have three input CSV files located in `/home/user/data/`:
1. `meta.csv`: Contains sensor metadata. Headers: `id,city`
2. `stream1.csv`: Contains sensor readings. Headers: `ts,id,val`
3. `stream2.csv`: Contains additional sensor readings. Headers: `ts,id,val`

Your objective is to build an ETL pipeline that integrates these sources, computes rolling statistics, and outputs a final JSON Lines file.

Requirements:

1. **DAG Orchestration (Makefile)**
Create a `Makefile` in `/home/user/` with the following targets to act as your DAG:
- `db-init`: Initializes a SQLite database at `/home/user/data/warehouse.db` and creates three tables (`meta`, `stream1`, `stream2`) corresponding to the CSV files.
- `db-import`: Bulk imports the data from the three CSV files into their respective SQLite tables. You may use the `sqlite3` CLI tool for this.
- `etl-process`: Compiles and runs a Rust project.
- `all`: Runs `db-init`, `db-import`, and `etl-process` in order.

2. **Rust Data Processing**
Create a Rust project in `/home/user/etl_pipeline` (which will be executed by `make etl-process`). The Rust program must:
- Connect to `/home/user/data/warehouse.db`.
- Union the data from `stream1` and `stream2`.
- Join the unioned stream data with the `meta` table on `id`.
- Calculate a mathematical rolling average of `val` for each sensor (`id`), ordered by `ts`. The rolling window should be **3 rows** (the current row and the 2 preceding rows). If fewer than 3 rows are available (i.e., at the start of the partition), calculate the average of the available rows.
- Export the final processed dataset to `/home/user/data/final_output.jsonl`.

3. **Output Format**
The output file `/home/user/data/final_output.jsonl` must be a JSON Lines file. Each line should be a JSON object with the following exact keys:
- `id` (integer)
- `city` (string)
- `ts` (string, e.g., "2023-01-01")
- `val` (float)
- `rolling_avg` (float, rounded to exactly 2 decimal places)

The lines in the JSONL file must be sorted by `id` ascending, then `ts` ascending.

Use whatever Rust crates you prefer (e.g., `rusqlite`, `polars`, `serde`). Assume the container runs a Debian-based Linux. You may install required system packages using `sudo apt-get` if necessary, though `sqlite3` and `cargo` are available.

Complete the pipeline such that running `make all` in `/home/user/` produces the correct `/home/user/data/final_output.jsonl`.