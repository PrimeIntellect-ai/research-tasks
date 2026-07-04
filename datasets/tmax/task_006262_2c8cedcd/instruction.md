You are tasked with building a state-reconciliation tool for a legacy configuration management system. 

The system collects configuration changes from thousands of servers and appends them to a central log file located at `/home/user/config_events.tsv`. Since these are legacy servers, their configuration values are transmitted using the `Windows-1252` (CP1252) character encoding, which occasionally includes characters like smart quotes or ellipses that are not valid ASCII or UTF-8.

Your goal is to write a Rust program that processes this time-series log and determines the most recent configuration state for every configuration key across the entire fleet.

**Input File Format (`/home/user/config_events.tsv`):**
The file is a tab-separated values (TSV) file without a header.
Columns:
1. `Timestamp`: Unix epoch integer (seconds).
2. `ServerName`: String (Valid UTF-8).
3. `ConfigKey`: String (Valid UTF-8).
4. `ConfigValue`: Raw bytes, encoded in Windows-1252.

**Requirements for your Rust program:**
1. Create a new Cargo project in `/home/user/config_tracker`.
2. Process `/home/user/config_events.tsv` in a streaming fashion (e.g., using `BufReader` line-by-line or chunk-by-chunk). You must not load the entire file into memory at once, as the production files are extremely large.
3. Group the events by `ConfigKey`.
4. For each `ConfigKey`, find the event with the highest `Timestamp`. (If timestamps are identical, the one appearing later in the file takes precedence).
5. Convert the `ConfigValue` of these latest events from Windows-1252 to valid UTF-8. You may use a third-party crate like `encoding_rs` to handle the conversion.
6. Write the final aggregated state to `/home/user/latest_state.csv`.
7. The output must be a standard CSV file (comma-separated).
8. The output must include a header row: `config_key,server_name,decoded_value`
9. The output rows must be sorted alphabetically by `config_key`.

Compile and run your Rust program so that the final `/home/user/latest_state.csv` is generated and ready for verification.