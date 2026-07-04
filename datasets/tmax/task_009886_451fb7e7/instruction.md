You are an open-source maintainer reviewing a Pull Request. A contributor has submitted a C++ translation of an old, slow Python script (`parse_logs.py`) to speed up log processing. However, the PR is broken and incomplete. 

Your workspace is located at `/home/user/pr_review`. 

The PR has the following issues that you must fix:
1. **Compilation Failure:** The `Makefile` is improperly configured. Running `make` fails because it does not correctly link all necessary object files. You must repair the `Makefile` so that `make` successfully builds the `log_parser` executable.
2. **Missing Translation:** The contributor left the function `is_valid_error_code` empty in `utils.cpp`. You must translate the logic for `is_valid_error_code` directly from `parse_logs.py` into C++ and implement it in `utils.cpp`.
3. **Memory Leak:** The C++ implementation in `log_parser.cpp` has a memory leak inside its main processing loop. Find and fix the memory leak. Ensure that your fix does not alter the intended functionality of the log parser.

**Verification Requirements:**
Once you have fixed the code, compiled the program, and removed the memory leak, perform the following verification steps:
1. Run the Python version: `python3 parse_logs.py dummy_logs.txt > /home/user/pr_review/py_out.txt`
2. Run your fixed C++ version: `./log_parser dummy_logs.txt > /home/user/pr_review/cpp_out.txt`
3. Profile the fixed C++ executable with Valgrind to prove the memory leak is resolved: 
   `valgrind --leak-check=full ./log_parser dummy_logs.txt 2> /home/user/pr_review/valgrind_report.txt`

The automated test suite will verify that:
- The `Makefile` builds `log_parser` correctly.
- `cpp_out.txt` exactly matches `py_out.txt`.
- `valgrind_report.txt` indicates exactly `0 bytes in 0 blocks` are definitely lost.