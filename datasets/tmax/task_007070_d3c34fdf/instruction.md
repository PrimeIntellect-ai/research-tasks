You are an incident response analyst investigating suspicious login telemetry. You have been given a messy JSON-lines log file containing user activity coordinates and timestamps.

The file is located at `/home/user/telemetry.jsonl`.
Each line is intended to be a JSON object with the following fields:
- `timestamp` (string): RFC3339 formatted time (e.g., "2023-10-12T14:32:01Z")
- `action` (string): The name of the action performed.
- `x` (float64): X coordinate.
- `y` (float64): Y coordinate.

However, the log forwarder had a bug where it occasionally wrote malformed Unicode escape sequences (e.g., `\u00XX`) into the `action` field, which breaks standard JSON parsers.

Your task is to write a Go program `/home/user/process.go` that:
1. Reads `/home/user/telemetry.jsonl` line by line.
2. Gracefully handles and skips any lines that fail to parse as valid JSON (due to the Unicode escape bug or other malformations).
3. Filters for records where the `action` field, when normalized to lowercase, equals exactly `login`. (Note: valid Unicode escapes like `log\u0069n` will be automatically resolved by a compliant JSON parser and should be treated as `login`).
4. Aligns the `timestamp` by truncating it to the top of the hour (e.g., `2023-10-12T14:32:01Z` becomes `2023-10-12T14:00:00Z`).
5. Computes the 2D Euclidean distance of the record's `x`, `y` coordinates from a fixed suspicious origin point at `x: 50.0`, `y: 50.0`. Formula: `sqrt((x-50.0)^2 + (y-50.0)^2)`.
6. Aggregates the data to compute the average distance of `login` events per hour.
7. Writes the results to a CSV file at `/home/user/hourly_stats.csv`.

The output CSV `/home/user/hourly_stats.csv` must:
- Have the exact header: `hour,login_count,avg_distance`
- Have the `hour` formatted as RFC3339 (e.g., `2023-10-12T14:00:00Z`).
- Have the `avg_distance` formatted to exactly two decimal places (e.g., `12.34`).
- Be sorted chronologically by the `hour` column.

Run your Go program to generate the CSV. You may use standard Go libraries only.