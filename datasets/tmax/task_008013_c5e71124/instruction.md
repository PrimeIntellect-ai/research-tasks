You are tasked with identifying a regression in a C++ data processing utility. 

The repository located at `/home/user/data_processor` contains the source code for `process_sensor_data.cpp`. This utility reads space-separated string values from standard input, decodes/cleans them (handling minor corruptions or encoding artifacts), and calculates their sum with high floating-point precision.

Between the git tags `v1.0` (known good) and `v2.0` (known bad), a developer introduced a regression spanning over 200 commits. The regression breaks two things:
1. It fails to recover from corrupted input prefixes (e.g., `#` or `*` characters before the number).
2. It introduces floating-point precision loss during parsing.

Your task is to:
1. Write a shell script to automate testing the C++ compilation and execution. 
2. Use `git bisect` to find the exact commit that introduced this regression.
3. To test the utility, you should decode the provided base64 test file `/home/user/test_input.b64` and pipe it to the compiled binary. The correct expected output sum for this specific test file is exactly `6.370370367`. The buggy versions will output a different number (like `4.24691...` or `0`).
4. Once you have identified the first bad commit, save its full 40-character SHA-1 hash to a file named `/home/user/bad_commit_hash.txt`.

Constraints:
- Do not modify the git history.
- Ensure your compiled binary is named `process_sensor_data` and is tested in the repository root.