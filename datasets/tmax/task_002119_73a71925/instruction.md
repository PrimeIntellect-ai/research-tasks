You are tasked with building a Go-based configuration change tracking system. We have a fleet of servers that continuously send configuration snapshots, but they send them in messy formats and often send duplicate data when nothing has changed.

Your goal is to write a Go application that processes this data, extracts key features, deduplicates unchanged states, and outputs a clean timeline of actual configuration changes. You must also deploy this application as a systemd service.

**Input Data:**
There is a file at `/home/user/input/configs.jsonl`. Each line is a JSON object representing a configuration snapshot from a server.
Fields:
- `server_id` (string)
- `reported_at` (can be an integer Unix timestamp, an RFC3339 string, or a "YYYY-MM-DD HH:MM:SS" string implicitly in UTC)
- `config_data` (a nested JSON object)

**Processing Requirements:**
Write a Go program in `/home/user/app/main.go` that does the following:
1. **Timestamp alignment:** Parse the `reported_at` field from its various formats and convert it to a standard Unix epoch timestamp (integer seconds).
2. **Feature extraction:** Extract the following specific fields from `config_data`:
   - `app_version` (string)
   - `max_conns` (integer)
   - `features.tls` (boolean)
3. **Hash-based deduplication:**
   - Create a canonical string representation of the extracted config: `"{app_version}|{max_conns}|{features.tls}"` (e.g., `"1.2.0|100|true"`).
   - Compute the SHA256 hash of this string (lowercase hex format).
   - For each `server_id`, sort the snapshots chronologically by the aligned Unix timestamp.
   - Iterate through the sorted snapshots for each server. If a snapshot's SHA256 hash is identical to the *immediately preceding* snapshot's hash for that same `server_id`, it is a duplicate (no actual config change occurred). Discard it. Keep the first occurrence of any new state.
4. **Output:**
   - Write the resulting deduplicated, sorted (grouped by `server_id` alphabetically, then by timestamp ascending) records to a CSV file at `/home/user/output/changelog.csv`.
   - The CSV must have the following header exactly: `server_id,timestamp,config_hash,app_version,max_conns,tls`
   - `tls` should be output as `true` or `false`.

**Deployment Requirements:**
1. Initialize a Go module in `/home/user/app`.
2. Build the Go application into a binary named `tracker` in `/home/user/app/`.
3. Create a systemd service file at `/etc/systemd/system/config-tracker.service` (you may use `sudo` for this part, assuming standard passwordless sudo access for the user if needed, or simply write the service to run as the `user`).
   - The service should execute `/home/user/app/tracker`.
   - Set `WorkingDirectory=/home/user/app`.
   - Run as user `user`.
4. Enable and start the `config-tracker.service`. It should execute the processing once and write the output file.

Ensure `/home/user/output/` exists.