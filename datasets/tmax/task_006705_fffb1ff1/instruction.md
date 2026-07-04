You are tasked with debugging a failing build in a Rust project located at `/home/user/chrono_shift`. 

The project is a custom date-time parsing library. Recently, the `cargo test` suite started failing with a panic. The repository has a short commit history, and the bug was introduced in a recent commit.

Your objectives are:
1. **Identify the regression:** Use git bisection to find the exact commit hash that introduced the bug. Write the full, unabbreviated commit hash of the first bad commit to a file named `/home/user/bad_commit.txt`.
2. **Diagnose the issue:** The bug involves a corrupted input handling failure related to timezone string parsing. The parser currently panics instead of returning a graceful error when encountering truncated or malformed timezone offsets.
3. **Fix the bug:** Modify `src/parser.rs` so that if the timezone slice operation fails (due to out-of-bounds or character boundary issues), the function returns `Err("Invalid Timezone")` instead of panicking.
4. **Verify:** Ensure that `cargo test` passes successfully after your fix.

Do not change the tests in `tests/test_parser.rs`. Only modify the implementation in `src/parser.rs`.