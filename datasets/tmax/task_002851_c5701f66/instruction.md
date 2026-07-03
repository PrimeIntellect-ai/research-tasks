You have inherited a legacy Rust codebase located at `/home/user/telemetry_parser`. This application is responsible for reading log files from various distributed services, parsing them, and combining them into a single chronological timeline. 

Currently, the application is failing in production. If you run `cargo run` inside the `/home/user/telemetry_parser` directory, it immediately panics. 

Your goals are to debug and fix the application to meet the following requirements:

1. **Format Parsing Edge-Case Repair**: Service C recently had a bug where it appended duplicate timezone offsets to its timestamps (e.g., `"2023-10-25T14:30:00Z+00:00"`). The current `chrono` parser panics when it encounters this. You must fix the parsing logic in `/home/user/telemetry_parser/src/main.rs` to handle these malformed timestamps by stripping the trailing `+00:00` if the string already contains a `Z`.
2. **Corrupted Input Handling**: Service B sometimes writes corrupted JSON lines (e.g., truncated data). Currently, `serde_json::from_str` unwraps the result and panics. You need to modify the code to gracefully handle these errors. Instead of crashing or dropping the data silently, append the exact raw corrupted string (with a trailing newline) to a file at `/home/user/corrupted_lines.log`. Skip the corrupted entries for the final timeline.
3. **Timeline Reconstruction**: After fixing the panics, the application just concatenates the logs. You must ensure the final output array of JSON objects is strictly sorted by the `timestamp` field in chronological order (oldest to newest).
4. **Minimal Reproducible Example**: Create a standalone Rust file at `/home/user/mre.rs`. This file should be an isolated reproducible example demonstrating the original `chrono` parsing panic on the string `"2023-10-25T14:30:00Z+00:00"`. It should compile with standard `rustc` (assuming `chrono` is available) and panic when executed. 

The application must output the final sorted timeline as a JSON array of objects to `/home/user/timeline_output.json`.

**Inputs**: The input log files are located in `/home/user/data/`. The application is currently hardcoded to read `/home/user/data/service_a.log`, `/home/user/data/service_b.log`, and `/home/user/data/service_c.log`.

Do not change the structure of the output JSON objects; only fix the panics, properly handle corrupted lines, and ensure the final array is chronologically sorted. Run `cargo build` and `cargo run` to verify your fixes.