You have been given a Python project in `/home/user/rust_log_parser` that processes Rust `cargo check` JSONL output. It uses a state machine to parse the structured data and extract compiler errors, specifically ownership and borrow checker errors.

However, the project is currently broken:
1. **Circular Import**: There is a circular dependency between `parser.py` and `models.py` which prevents the script from running.
2. **State Machine Bug**: The state machine in `parser.py` correctly extracts errors, but it drops the very last error in the stream because it never transitions out of the `IN_ERROR` state when the log file abruptly ends.

Your task:
1. Fix the circular import issue so that `main.py` runs without `ImportError`. You may refactor the functions as needed, but do not change the data structures.
2. Fix the state machine in `LogParser` (inside `parser.py`) so that it doesn't lose the last error. You should add a `finalize()` method to `LogParser` that handles the end-of-stream logic (appending the final error if the state is still `IN_ERROR`). Make sure `main.py` calls this `finalize()` method after reading all lines.
3. Once the code is fixed, run the parser on the provided log file to generate the final output:
   ```bash
   cd /home/user/rust_log_parser
   python main.py cargo_errors.jsonl summary.json
   ```

Requirements:
- The final parsed errors must be written to `/home/user/rust_log_parser/summary.json`.
- The `summary.json` file must contain a valid JSON array of all the parsed errors (it should have exactly 2 errors if parsed correctly).