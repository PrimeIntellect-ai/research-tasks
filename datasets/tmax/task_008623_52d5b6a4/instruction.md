You are tasked with building a Go-based configuration change tracker. 

We have a system that periodically dumps its configuration state into the `/home/user/config_dumps/` directory. Due to legacy reasons, these dumps are in two different formats: JSON (`.json`) and plain text key-value pairs (`.txt`). The system dumps the configuration every minute, even if nothing changed, resulting in a lot of redundant data.

Your goal is to write a Go program at `/home/user/tracker.go` that reads these files in parallel, extracts specific configuration values, deduplicates redundant consecutive states using hashing, and outputs a time-series CSV of the actual configuration changes.

Here are the requirements:
1. **Input Directory**: `/home/user/config_dumps/`. The files are named `dump_<timestamp>.json` and `dump_<timestamp>.txt`. The `<timestamp>` is an integer representing the Unix epoch time.
2. **Extraction**: From each file, extract three fields:
   - `db_host` (string)
   - `db_port` (integer)
   - `max_connections` (integer)
   *Note: In `.txt` files, these are formatted as `key=value` on separate lines. In `.json` files, they are standard JSON keys.*
3. **Parallel Processing**: You must use Go concurrency (goroutines) to read and parse the files.
4. **Hashing & Deduplication**:
   - For each extracted configuration, compute the SHA-256 hash of the string formatted exactly as: `db_host:db_port:max_connections`
   - Order the parsed configurations chronologically by their filename timestamp.
   - Deduplicate consecutive identical configurations. A configuration is considered redundant if its hash matches the hash of the *immediately preceding* chronological configuration.
5. **Output**: Write the deduplicated time-series data to `/home/user/config_history.csv` with the exact following header:
   `timestamp,db_host,db_port,max_connections,config_hash`
   *Output the hash as a lowercase hex string.*

Ensure you initialize a Go module in `/home/user` if necessary, and compile/run your code to produce the final CSV.