You are tasked with building a configuration management tracking tool in Rust. As a system administrator, you have configuration dumps from three different points in time, each in a different format. You need to read these files, normalize the configuration keys, and generate a summary report of how the configuration has changed over time.

The three configuration files are located at:
1. `/home/user/data/config_v1.json` (Oldest)
2. `/home/user/data/config_v2.csv`
3. `/home/user/data/config_v3.ini` (Newest)

Your task is to write and execute a Rust program (create a cargo project in `/home/user/config_tracker`) that does the following:

1. **Multi-format reading**: Read the key-value pairs from all three files.
   - The JSON file contains a flat dictionary of keys and values (all strings).
   - The CSV file has headers `key` and `value`.
   - The INI file has a `[default]` section containing the key-value pairs.
2. **Tokenization and Normalization**: Normalize every key by converting it entirely to lowercase, and replacing all hyphens (`-`) with underscores (`_`). 
3. **Reshaping and Grouping**: Group the values for each normalized key in chronological order (v1 -> v2 -> v3). If a key is missing in a specific version, skip that version for that key.
4. **Summary Statistics**: For each normalized key, calculate:
   - `num_changes`: The number of times the value changed between consecutive versions where the key was present. (The initial appearance of a key does not count as a change).
   - `first_value`: The earliest recorded value for the key.
   - `latest_value`: The most recently recorded value for the key.
5. **Output**: Write the results to a CSV file at `/home/user/output/config_summary.csv` with the headers `normalized_key,num_changes,first_value,latest_value`. The rows must be sorted alphabetically by `normalized_key`.

You may use standard Rust crates (e.g., `serde`, `serde_json`, `csv`, `rust-ini`) by adding them to your `Cargo.toml`. Create the output directory if it doesn't exist. After writing the code, compile and run it so that the output CSV is generated.