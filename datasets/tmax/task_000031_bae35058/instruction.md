You are acting as a support engineer investigating a bug reported by a customer. The customer uses our Rust-based job submission tool, `rusty-dispatcher`, to send files to a cluster of worker containers. They are reporting that files are randomly being dropped or failing to process.

You have been provided with two things:
1. An archive of recent logs from the worker containers, located at `/home/user/logs/` (these have already been extracted).
2. The source code for the dispatcher tool, located at `/home/user/rusty-dispatcher/`.

Your investigation tasks:

**Phase 1: Diagnostic Data Collection & Timeline Reconstruction**
The logs in `/home/user/logs/` come from multiple containers (`node_alpha.log`, `node_beta.log`, etc.). The customer isn't sure which files failed.
1. Parse across all the log files to find every log entry marked as `ERROR`.
2. Extract the exact absolute file paths that failed to process.
3. Save this list of failed file paths as a strictly formatted JSON array of strings in `/home/user/diagnostics/failed_files.json`. 
*(Ensure the `/home/user/diagnostics/` directory exists, creating it if necessary).*

**Phase 2: Intermittent Bug Reproduction (Regression Test)**
Based on the file paths you extracted, you should notice a pattern regarding why these specific files failed (hint: look at the characters in the filenames). 
1. Navigate to `/home/user/rusty-dispatcher/`.
2. In the `src/processor.rs` file, there is a function `pub fn execute_worker_job(filepath: &str) -> Result<(), String>`.
3. Write a standard Rust unit test at the bottom of `src/processor.rs` named `test_filename_with_spaces_regression`.
4. This test must programmatically create a temporary file whose name contains at least one space, call `execute_worker_job` on that file's absolute path, and assert that it returns `Ok(())`. (Do not use `#[should_panic]` or expect an error—the goal of the fixed code is to succeed).

**Phase 3: Root Cause Fix**
1. Fix the bug in `src/processor.rs`'s `execute_worker_job` function. The current implementation unsafely concatenates the filepath into a shell string, causing it to break when filenames have spaces or special characters.
2. Refactor the `std::process::Command` usage so that it bypasses the shell string concatenation vulnerability and safely passes the file path as a direct argument to the `mock_worker.sh` script.
3. Ensure that running `cargo test` in `/home/user/rusty-dispatcher/` passes successfully.

Do not change the signature of `execute_worker_job`. The test environment includes a dummy `mock_worker.sh` script in `/usr/local/bin/` (or locally in the project path depending on the setup) that your Rust code calls.