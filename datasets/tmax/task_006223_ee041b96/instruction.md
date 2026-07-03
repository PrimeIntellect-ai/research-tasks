You are a DevOps engineer tasked with debugging a regression in a Rust-based log parsing utility. 

We have a local Git repository at `/home/user/log_processor`. This utility reads a log file and outputs a summary of log levels.
Recently, a regression was introduced. When running the tool on `/home/user/input.log`, it is supposed to report exactly 100 total log entries. On the `v1.0.0` tag, it processes all 100 entries correctly. However, on the `main` branch, it silently drops some entries and reports a lower number.

Your tasks are to:

1. **Assertion-based intermediate validation:** Write a test script at `/home/user/bisect_test.sh` that builds the Rust project (using `cargo build --release`), runs it against `/home/user/input.log`, and asserts that the output reports exactly 100 entries. The script must exit with `0` if the count is correct (good) and `1` if the count is incorrect (bad). Make sure the script is executable.
2. **Git bisection:** Use `git bisect` along with your test script to automatically find the exact commit hash that introduced the regression between the `v1.0.0` tag (good) and `main` (bad).
3. **System call tracing:** The regression was caused by a developer adding a feature that checks for an external configuration file. If this file is missing, the program silently skips certain log lines instead of panicking. Use `strace` on the compiled binary of the *bad* commit to identify the exact absolute path of this missing configuration file (look for a failed `openat` or `open` syscall resulting in `ENOENT`).
4. **Reporting:** Create a JSON file at `/home/user/debugging_report.json` with the following structure:
```json
{
  "bad_commit": "<full_40_character_commit_hash>",
  "missing_file": "<absolute_path_to_the_missing_config_file>"
}
```

Constraints:
- Do not modify the Git history.
- The repository must be left in its original state or detached at the bad commit (do not leave a bisect running).