You are tasked with resolving a compilation error in a multi-file Rust web server project located at `/home/user/rust_server`. The compilation fails due to a thread-safety issue (a critical web security flaw: a race condition in the session management state). 

You have been provided with a patch file from a previous Go service that fixes a similar vulnerability using Go concurrency patterns. This file is located at `/home/user/go_fix.patch`.

Your objective is to write a Python script at `/home/user/fix_rust.py` that performs the following tasks:
1. **Custom Data Structure & Patch Processing:** Implement a custom data structure (e.g., a `Hunk` and `DiffFile` class) in Python to manually parse the unified diff in `/home/user/go_fix.patch`. 
2. **Analysis:** Using your custom data structure, programmatically extract the name of the struct field (e.g., `sessions`) that was protected by a mutex lock in the Go patch.
3. **Patching Rust:** Identify the equivalent `AppState` struct and its failing insertion logic in `/home/user/rust_server/src/main.rs`. Have your Python script automatically modify the `main.rs` file so that:
   - The vulnerable field is wrapped in a `std::sync::Mutex`.
   - The initialization of the field is correctly updated to use `Mutex::new`.
   - The thread execution block is updated to acquire the `.lock().unwrap()` before mutating the session map.
4. **Verification:** Your Python script must run `cargo check` in the `/home/user/rust_server` directory. If the compilation succeeds without errors, your script must create a file at `/home/user/status.txt` containing the exact word `SECURED`.

Constraints:
- You must use Python to write the parsing and patching logic.
- Do not just use `sed` or `awk` from bash to fix the Rust code; your `/home/user/fix_rust.py` script must handle the reading, parsing of the Go diff, and the patching of the Rust file.
- Assume standard Python 3 libraries only.
- Ensure the final Rust code compiles cleanly.