You are a script developer tasked with creating a custom Bash utility for a CI/CD pipeline that automatically detects and patches basic Rust ownership errors and prepares a cross-compiled release package.

We have a simulated Rust project in `/home/user/project`. 
A previous CI step attempted to cross-compile this project for `x86_64` and `arm64`, and wrote the compiler stderr logs to:
- `/home/user/project/build_x86.log`
- `/home/user/project/build_arm.log`

Your goal is to write a Bash script at `/home/user/ci_tool.sh` that performs the following automated steps when executed:

1. **Analyze the Build Logs**: Check both `build_x86.log` and `build_arm.log` for the Rust borrow checker error `error[E0382]: borrow of moved value`.
2. **Auto-Patching**: If `E0382` is detected in either log, find the line where the value was moved. In standard `rustc` output, there is a note like `|              -- value moved here` on the line *below* the actual code that caused the move. The log shows the snippet. For this task, locate the exact line number of the code where the move occurred (in the provided log, this will be line 3: `3 |     let s2 = s1;`). 
   Modify `/home/user/project/src/main.rs` at that exact line number to append `.clone()` before the semicolon. For example, `let s2 = s1;` should become `let s2 = s1.clone();`. Do not hardcode the line number `3` in your script—your script must dynamically extract the line number from the log where the move occurred (the line number printed right before `|     let s2 = s1;`).
3. **Reporting**: Generate a report file at `/home/user/project/ci_report.log` with exactly the following format:
   ```
   [x86] Status: <STATUS>
   [arm] Status: <STATUS>
   Patched line: <LINE_NUMBER>
   ```
   If a log contained the `E0382` error, its `<STATUS>` should be `FAILED_BUT_FIXED`. If no error was found, `<STATUS>` should be `SUCCESS`. `<LINE_NUMBER>` should be the dynamically extracted line number where the patch was applied (or `NONE` if no patch was needed).
4. **Packaging**: Create a gzipped tarball of the `/home/user/project/src` directory and save it to `/home/user/project/src_archive.tar.gz`.

To complete this task, write the `/home/user/ci_tool.sh` script, make it executable, and run it so that all artifacts (`ci_report.log`, the modified `main.rs`, and `src_archive.tar.gz`) are generated.