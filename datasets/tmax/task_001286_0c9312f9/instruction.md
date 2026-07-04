You are a data engineer tasked with building a secure data processing pipeline for telemetry CSV files. Our downstream systems are vulnerable to CSV injection and buffer overflows, so you must implement a strict sanitization and aggregation pipeline in Go.

You have been provided with a vendored copy of the `gocsv` package located at `/app/vendor/gocsv`. Unfortunately, a junior developer made an unauthorized change to it, and it currently panics or fails to build. 

Your tasks are:

1. **Fix the Vendored Package:**
   Inspect the vendored package at `/app/vendor/gocsv`. Find and remove the deliberate perturbation (a panic or syntax error injected into `gocsv.go` or `utils.go`) so the package works correctly.

2. **Implement the Pipeline:**
   Create a Go program at `/home/user/pipeline/main.go`. Initialize a Go module in `/home/user/pipeline` and use a `replace` directive to point `github.com/gocarina/gocsv` to your fixed vendored path (`/app/vendor/gocsv`).

   Your Go program must support two subcommands:

   **Command A: `validate <input_csv_path>`**
   This command acts as a strict security filter. It must read the CSV file and exit with code `0` if the file is completely clean, or exit with code `1` if it detects ANY malicious rows. 
   A CSV is considered "evil" (malicious) if any field in any row meets these criteria:
   - Starts with `=`, `+`, `-`, or `@` (CSV injection attempt)
   - Contains a Null byte (`\x00`)
   - Has a length strictly greater than 500 characters.

   **Command B: `transform <input_csv_path> <output_json_path>`**
   This command extracts features and performs windowed aggregation on clean files.
   The input CSV has headers: `timestamp,sensor_id,value,notes`. `value` is a float64.
   For each unique `sensor_id`, calculate a rolling average of the `value` over a window of the last 3 chronological events (or fewer if 3 haven't occurred yet).
   Write the output as a JSON array of objects to `<output_json_path>`, containing: `timestamp` (string), `sensor_id` (string), `original_value` (float64), `rolling_avg` (float64). Preserve the original chronological order of the rows.

Ensure your code is efficient, handles errors gracefully, and accurately outputs the JSON format. Our automated security suite will rigorously test your `validate` command against malicious and clean datasets.