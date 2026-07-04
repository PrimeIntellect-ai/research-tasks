You are a data scientist cleaning up a messy dataset of sensor readings. You have a raw text file located at `/home/user/raw_measurements.txt`.

The file contains experimental data in a messy, wide format. Each line represents a batch of sensor readings, formatted as follows:
`<Sample_ID> | <measurement_id>: <value>, <measurement_id>: <value>, ...`

For example:
`X-1 | p1: 10.0C, p2: 12.5 C, p1: 9.0C, p3: N/A`

Your task is to write a Rust program that processes this file and converts it into a clean, long-format CSV file. 

Requirements for your Rust program:
1. **Extraction & Reshaping**: Parse each line, split the `Sample_ID` from the measurements, and reshape the wide list of key-value pairs into a long format (one row per valid measurement).
2. **Cleaning & Normalization**: 
   - Extract the numeric value from the `<value>` string. 
   - The values may contain spaces and the letter 'C' or 'c' (representing Celsius). You must strip these out.
   - If a value cannot be parsed as a standard 64-bit float after stripping spaces and 'C'/'c' (e.g., "N/A", "err"), silently discard that specific measurement.
3. **Deduplication / Aggregation**: The same `Sample_ID` and `measurement_id` combination may appear multiple times (either on the same line or across different lines). For each unique `(Sample_ID, measurement_id)` pair, keep only the **maximum** numeric value.
4. **Parallel Processing**: You must use the `rayon` crate to process the lines of the input file in parallel.
5. **Output**: Write the final, cleaned data to `/home/user/cleaned_measurements.csv`. 
   - The CSV must have the header exactly as: `id,measurement,value`
   - The rows must be sorted alphabetically first by `id`, and then alphabetically by `measurement`.
   - Format the float values to 1 decimal place (e.g., `10.5`).

Setup your Rust project in `/home/user/cleaner` (e.g., using `cargo new`). You are free to add dependencies like `rayon` to your `Cargo.toml`. When finished, run your program so that `/home/user/cleaned_measurements.csv` is generated successfully.