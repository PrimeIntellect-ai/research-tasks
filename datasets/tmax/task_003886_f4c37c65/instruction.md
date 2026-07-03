You are a support engineer investigating a bug reported by a customer. They are using a C++ command-line tool that parses URL-like query strings into key-value pairs. 

The customer reported that certain malformed queries cause the tool to crash abruptly with a `std::out_of_range` exception, which is disrupting their data processing pipeline.

Your tasks are:
1. Locate the buggy source code at `/home/user/query_processor.cpp`.
2. Discover the crash: Write a simple fuzzer or manually test inputs to find a query string that triggers the `std::out_of_range` exception. The crashing input involves standard query characters (letters, `=`, `&`). Save the exact crashing string you found into a file named `/home/user/crashing_input.txt`.
3. Fix the bug in `/home/user/query_processor.cpp`: If a query parameter token (separated by `&`) does not contain an `=`, the tool should treat the entire token as the key and assign it an empty string for the value, rather than crashing.
4. Compile your fixed program to `/home/user/query_processor` using `g++ -O2 -std=c++17`.
5. Create a regression test: Write a bash script at `/home/user/regression_test.sh` that executes `/home/user/query_processor` passing the contents of `/home/user/crashing_input.txt` as the first argument. The script must exit with code `0` if the program succeeds and does not crash, and `1` if it fails. Ensure the script is executable.
6. Generate a diagnostics log: Run your fixed compiled program with the input from `/home/user/crashing_input.txt` and redirect the standard output to `/home/user/diagnostics.log`.

The final system state should have:
- The fixed source code in `/home/user/query_processor.cpp`
- The compiled binary at `/home/user/query_processor`
- The crashing input in `/home/user/crashing_input.txt`
- The executable test script at `/home/user/regression_test.sh`
- The output of the fixed run in `/home/user/diagnostics.log`