You are an automation specialist tasked with modernizing a critical data pipeline. 

We have a legacy compiled executable located at `/app/legacy_aggregator`. This binary processes raw telemetry logs, but it is unacceptably slow and its source code was lost years ago. We know it performs several key operations on the data:
1. **Regex Extraction**: Parses unstructured log lines to extract a timestamp, sensor ID, reading value, and a diagnostic code.
2. **Constraint Validation**: Drops corrupted or out-of-bounds readings based on undocumented constraints.
3. **Reshaping (Long to Wide)**: Pivots the data so that each row represents a time window, with individual sensors as columns.
4. **Aggregation**: Calculates summary statistics (e.g., means) for each sensor within the time window.

Your objective is to reverse-engineer the logic of the black-box binary by testing it against the provided sample data `/home/user/sample.log`. You must deduce the extraction rules, validation constraints, the specific time-window aggregation method, and the exact output schema.

Once you understand the pipeline, write a highly optimized Python script at `/home/user/fast_aggregator.py` that implements the exact same data transformations. 

**Requirements:**
- Your script must be invoked as: `python3 /home/user/fast_aggregator.py <input_log_path> <output_csv_path>`
- The output CSV must perfectly match the schema, sorting, and aggregated values produced by `/app/legacy_aggregator <input_log_path>`.
- The legacy binary is extremely slow. Your Python implementation will be evaluated against a massive held-out dataset. It must process the data and produce identically accurate results while achieving a minimum **runtime speedup of 20x** compared to the legacy binary.

Use the sample data to iterate and ensure your Python script replicates the binary's behavior exactly, but much faster.