You are acting as a script developer working on a log processing utility. 

We have a fast log-merging engine written in Rust, located at `/home/user/merger.rs`. It takes two log files as arguments, merges their lines, sorts them alphabetically, and prints the result with a header.
However, the original developer left a Rust ownership and borrow checker bug in the code, preventing it from compiling.

Your tasks are as follows:

1. **Fix the Rust Bug:** 
   Analyze and fix the ownership/borrow checker bug in `/home/user/merger.rs`. Ensure the program's logic remains intact (it must still print the header and the sorted lines).
   Compile the fixed code into an executable named `/home/user/merger` using `rustc`.

2. **Create a Bash Integration Test Runner:**
   Write a Bash script at `/home/user/run_tests.sh`. The script must do the following:
   - Iterate through all directories matching `/home/user/tests/case*` in alphabetical order.
   - Each test case directory contains `input1.txt`, `input2.txt`, and `expected.txt`.
   - For each directory, run the compiled `/home/user/merger` on `input1.txt` and `input2.txt`, saving the stdout to `output.txt` inside that same directory.
   - Use the `diff` command to compare `output.txt` against `expected.txt`.
   - If they match exactly, append the line `[PASS] <directory_name>` to `/home/user/test_report.log` (e.g., `[PASS] case1`).
   - If they differ, append `[FAIL] <directory_name>` to `/home/user/test_report.log`.

3. **Run the Tests:**
   Execute your script `/home/user/run_tests.sh` to generate the `/home/user/test_report.log`.

Constraints:
- You must write the Bash script yourself.
- Do not hardcode the number of test cases; dynamically iterate over `/home/user/tests/case*`.
- The final verification will check the compiled Rust binary, the Bash script, and the exact contents of `/home/user/test_report.log`.