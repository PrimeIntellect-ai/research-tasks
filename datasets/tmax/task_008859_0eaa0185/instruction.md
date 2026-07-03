You are assisting a release manager in preparing a critical deployment of a high-performance Python package called `log_parser_accel`. This package contains a fast state-machine-based log parser written in Rust, wrapped as a Python C-extension via `setuptools-rust` and `PyO3`.

Unfortunately, the previous developer left the repository in a broken state in `/home/user/log_parser_accel`:
1. **Broken Build Configuration:** The `setup.py` is incomplete and fails to build the shared library correctly. It does not properly link or declare the Rust extension for ABI compatibility.
2. **Borrow Checker Errors:** The Rust implementation in `src/lib.rs` (a state machine parser) fails to compile due to ownership and lifetime issues. The developer tried to store string slices (`&str`) in the parsed `LogEntry` struct returned to Python, causing a borrow checker violation when the local string buffer is dropped.
3. **Missing Python Wrapper:** The package needs to be installed, and a validation script must be written to verify it works.

Your tasks are:
1. Fix `setup.py` to properly use `RustExtension` from `setuptools_rust` to build the `log_parser_accel` module.
2. Fix the Rust code in `src/lib.rs` to resolve the ownership/borrow checker errors. You should modify the structs to own their data (e.g., using `String` instead of `&str`) so they can safely cross the ABI boundary into Python.
3. Build and install the package in the local environment (`pip install -e .`).
4. Write a Python script at `/home/user/run_parser.py` that imports `log_parser_accel`, reads the log file located at `/home/user/server.log`, and uses the `Parser` class to parse it.
5. The parser's `parse_line` method returns a `LogEntry` object with `level` and `message` properties if a complete log is parsed, or `None` if it's transitioning states. Collect all successfully parsed entries into a list of dictionaries (e.g., `[{"level": "ERROR", "message": "Disk full"}, ...]`) and save it as a JSON array to `/home/user/release_results.json`.

Ensure your final JSON file exactly matches the parsed structure from the provided `server.log`.