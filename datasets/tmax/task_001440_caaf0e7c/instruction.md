You are managing a global configuration tracker. Different servers log their configuration changes to a central system, but the logs are messy, contain duplicates, and have inconsistent timestamps. 

A Rust Cargo project has been set up at `/home/user/config_tracker`. It contains an input file `/home/user/config_tracker/input.jsonl` with raw configuration logs. 

Each line in `input.jsonl` is a JSON object with the following fields:
- `server_id` (string)
- `timestamp` (string or integer): Can be either a Unix epoch timestamp (integer, seconds) or an RFC 2822 formatted date string (e.g., "Tue, 1 Jul 2003 10:52:37 +0200").
- `description` (string): A multi-lingual description of the change.
- `config_payload` (string): A JSON string representing the new configuration.

Your task is to write the Rust application in `/home/user/config_tracker/src/main.rs` to process this file and write the result to `/home/user/config_tracker/output.jsonl`.

The processing must perform the following steps:
1. **Timestamp Alignment**: Parse the `timestamp` field and convert it to a strict ISO 8601 UTC string in the format `YYYY-MM-DDTHH:MM:SSZ`.
2. **Data Validation**: 
   - The `description` field must NOT exceed 40 Unicode characters (count characters, not bytes). If it exceeds 40 characters, discard the log entry.
   - The `config_payload` must be a valid JSON object. If it cannot be parsed as a valid JSON object, discard the log entry.
3. **Hash-based Deduplication**: Multiple servers might report the exact same configuration change. Compute the SHA-256 hash of the concatenated string: `description` + `config_payload`. Use this hash to deduplicate entries. If multiple valid entries produce the same hash, keep ONLY the entry with the *earliest* chronological timestamp. (If there is a tie in timestamps, keep the one that appeared first in the input file).
4. **Output**: Write the valid, deduplicated entries to `/home/user/config_tracker/output.jsonl`. Each line must be a JSON object with the fields: `server_id`, `timestamp` (the aligned UTC string), `description`, and `config_payload`. The output file MUST be sorted chronologically by the new `timestamp` string in ascending order.

The project already has `serde`, `serde_json`, `chrono`, and `sha2` in its `Cargo.toml`. Compile and run your code to generate the `output.jsonl`.