You are a log analyst investigating suspicious patterns in our application logs. We have been receiving logs containing SQL injection attempts, and we need a reliable filter to sanitize these logs before they are loaded into our data warehouse.

Your task has two parts:

1. **Fix the Vendored Dependency**
We use a custom, proprietary crate for parsing our specific log timestamps, located at `/app/vendored/log-chrono-0.1.5`. Unfortunately, the package is currently broken. Its `Cargo.toml` contains a deliberate perturbation (an invalid `build-dependencies` path pointing to a non-existent directory). You must fix this `Cargo.toml` so the package compiles.

2. **Build the Log Sanitizer**
Create a new Rust project at `/home/user/log_sanitizer`.
This project must use the locally vendored `log-chrono` crate (path: `/app/vendored/log-chrono-0.1.5`).
Write a Rust program that takes two command-line arguments: an input file path and an output file path.
- The input file contains JSON Lines (one JSON object per line). Each object has `timestamp`, `level`, and `message` fields.
- Your program must read the input file and write to the output file.
- You must DROP (exclude from output) any log line where the `message` field contains any of the following SQL injection patterns (case-insensitive):
  - `union select`
  - `drop table`
  - `or 1=1`
  - `--`
- For all other benign logs, you must preserve the exact JSON line and write it to the output file.
- Before checking the message, you must parse the `timestamp` field using the `log_chrono::parse_ts` function from the vendored crate. If a timestamp cannot be parsed (function returns an Err), the log line should also be dropped.

To successfully complete the task, your compiled binary must be executable via a wrapper script you create at `/home/user/run_filter.sh`. The script should accept two arguments: `<input_file>` `<output_file>`, and invoke your Rust program.

We will test your script against a hidden adversarial corpus of evil logs (which must be 100% rejected) and a clean corpus of normal logs (which must be 100% preserved).