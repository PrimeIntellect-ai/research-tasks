You are a data engineer responsible for a new time-series ETL pipeline. We receive IoT sensor data from two different systems, both outputting CSV files. You need to write a Rust program to read these files, validate the data, deduplicate it using a cryptographic hash, and load it into a SQLite database.

I have created a skeleton Rust project at `/home/user/etl_pipeline` with the necessary dependencies (`csv`, `rusqlite`, `md5`) already in the `Cargo.toml`.

Your task is to write the Rust code in `/home/user/etl_pipeline/src/main.rs` to perform the following ETL steps:

1. **Extract & Union**: Read from two CSV files: `/home/user/data/source_a.csv` and `/home/user/data/source_b.csv`. Both have no headers and the following format:
   `timestamp (String), sensor_id (String), metric_type (String), value (f64)`

2. **Validation (Quality Gate)**:
   Filter out any rows that do not meet these conditions:
   - If `metric_type` is `"temp"`, the `value` must be between `-40.0` and `80.0` (inclusive).
   - If `metric_type` is `"hum"`, the `value` must be between `0.0` and `100.0` (inclusive).
   - Any other `metric_type` should be rejected.

3. **Hash-based Deduplication**:
   For each valid row, compute the MD5 hash of the concatenated string: `timestamp + sensor_id + metric_type`.
   Represent the hash as a lowercase hex string.
   Use this hash to deduplicate rows (if multiple rows generate the same hash, keep only the first one encountered).

4. **Load (Database Bulk Export)**:
   Create a SQLite database at `/home/user/data/measurements.db`.
   Create a table named `metrics` with the schema:
   `CREATE TABLE metrics (hash TEXT PRIMARY KEY, timestamp TEXT, sensor_id TEXT, metric_type TEXT, value REAL)`
   Insert the deduplicated, valid rows into this table. Ensure your program compiles and runs successfully using `cargo run` in the `/home/user/etl_pipeline` directory.