You are a platform engineer maintaining a CI/CD pipeline. A recent pipeline run failed, and you need to build a Bash-based tool to analyze the logs, extract data, evaluate metrics, and fix a broken build configuration.

All necessary files are located in `/home/user/ci_data/` (which you will need to process).

Your task is to write a Bash script at `/home/user/pipeline_tool.sh` that processes the pipeline data and outputs a precise report. The script must perform the following actions:

1. **URL Parameter Parsing**: 
   Read `/home/user/ci_data/build.log`. The first line contains a webhook URL that triggered the build. Extract the value of the `commit_sha` query parameter.
   
2. **Rust Borrow Checker Error Extraction**:
   The `build.log` also contains output from a failed Rust compilation. Extract the specific Rust error code (e.g., `E0123`) and the exact line number in `src/main.rs` where the error occurred.

3. **Expression Parsing and Evaluation**:
   Read `/home/user/ci_data/metrics.txt`. This file contains several key-value pairs where the value is a mathematical expression (e.g., `test_duration=45+12*3`). Evaluate these expressions.

4. **Report Generation**:
   Your script must generate a report at `/home/user/report.txt` with the exact following format:
   ```
   COMMIT_SHA: <extracted_sha>
   RUST_ERROR_CODE: <extracted_error_code>
   RUST_ERROR_LINE: <extracted_line_number>
   test_duration: <evaluated_result>
   coverage: <evaluated_result>
   ```

5. **C Makefile Repair**:
   There is a broken Makefile at `/home/user/ci_data/Makefile.broken`. It has two issues:
   - It uses 4 spaces instead of a tab for the command indentation.
   - It uses an invalid GCC flag `-wall` instead of the correct `-Wall`.
   Create a corrected version at `/home/user/ci_data/Makefile.fixed`. Do this via your script or standard shell commands.

Requirements:
- Ensure `/home/user/pipeline_tool.sh` is executable and runs successfully without arguments, reading from `/home/user/ci_data/` and creating `/home/user/report.txt`.
- Use only standard bash built-ins, coreutils, and tools like `grep`, `sed`, `awk`, or `bc`.