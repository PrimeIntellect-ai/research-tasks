You are a Build Engineer managing a mathematical evaluation tool named `mathtool`. The project consists of a C-based command-line utility that parses and evaluates mathematical expressions, and a Python-based integration testing suite. 

Currently, the build is failing, the C program has a critical memory safety issue causing undefined behavior, and the test pipeline is incomplete.

Your objectives are to fix the project, run the tests, and package the release artifacts.

Here is the current state of the project located at `/home/user/mathtool`:

1. **Build System (Linking Error):**
   The `/home/user/mathtool/Makefile` has a configuration issue. It compiles the object files but fails during the linking stage with undefined reference errors related to mathematical functions. Fix the `Makefile` so that running `make` successfully produces the `mathtool` executable in the `/home/user/mathtool/` directory.

2. **Memory Safety & Undefined Behavior:**
   There is a bug in `/home/user/mathtool/src/parser.c`. When extracting numerical tokens from the expression string, the code dynamically allocates a buffer but fails to properly null-terminate it before converting it to a double. This leads to undefined behavior, occasionally returning garbage values or causing memory corruption. Identify and fix this memory safety issue. 

3. **Test Fixture Setup:**
   Create a JSON test fixture at `/home/user/mathtool/tests/fixture.json` containing an array of test cases. Each test case must be a JSON object with two keys: `"expression"` (a string) and `"expected"` (a float). 
   You must include exactly these three test cases:
   - Expression: `"3 + 5 * 2"`, Expected: `13.0`
   - Expression: `"pow(2, 3) - 1"`, Expected: `7.0`
   - Expression: `"10.0005 + 0.0005"`, Expected: `10.001`

4. **Integration Testing:**
   Complete the Python test script located at `/home/user/mathtool/tests/test_runner.py`. The script currently loads the JSON fixture but is missing the logic to actually invoke the `mathtool` binary. 
   You must add the code to:
   - Use the `subprocess` module to execute `../mathtool "<expression>"`.
   - Read the standard output (which will be a single floating-point number string).
   - Compare the output to the expected value (allow a tolerance of `0.0001`).
   - Write the results to `/home/user/mathtool/test_report.json` in the following format:
     ```json
     {
       "total": 3,
       "passed": 3,
       "failed": 0
     }
     ```
   Run your completed test script to generate `test_report.json`.

5. **Artifact Packaging:**
   Once everything is fixed and the tests pass, create a compressed tarball at `/home/user/artifact.tar.gz` containing exactly two files at its root level (do not include parent directories in the tar archive):
   - `mathtool` (the compiled binary)
   - `test_report.json`

Ensure all file paths and formats exactly match the instructions above.