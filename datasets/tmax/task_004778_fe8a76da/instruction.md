I am a DevOps engineer, and our custom Rust-based log parsing utility keeps crashing when processing yesterday's server logs. The panic trace tells us there is an "index out of bounds" or "unwrap on None" error, but it doesn't tell us *which* specific log line from the 10,000+ line log file is causing the issue.

The project is located at `/home/user/log-parser`.
The log file is located at `/home/user/logs/server.log`.
The parser can be run via `cargo run -- /home/user/logs/server.log`.

Your tasks are:
1. **Identify the Crashing Input:** Use delta debugging, interactive debugging (e.g., `gdb` or `rust-gdb`), or intermediate print statements to find the exact log line causing the application to crash. Write the exact content of this line to `/home/user/bug_report.txt` in the exact format: `Line content: <exact_line_text>`. Do not include a trailing newline in the line text itself if it can be avoided, just the raw text of the log line.
2. **Fix the Bug:** Modify the Rust code in `/home/user/log-parser/src/main.rs` so that it safely ignores malformed lines (lines with fewer than 4 space-separated parts) instead of panicking. After your fix, `cargo run -- /home/user/logs/server.log` must complete with an exit code of 0 and print the total number of successfully parsed lines.
3. **Add a Regression Test:** Add a unit test function named `test_malformed_line` in `/home/user/log-parser/src/main.rs` that explicitly calls the internal `parse_line` function with the malformed line you found, asserting that it returns `None` (or handles the error gracefully as per your fix) instead of panicking. `cargo test` must run successfully.

Ensure your code compiles and passes all tests before finishing.