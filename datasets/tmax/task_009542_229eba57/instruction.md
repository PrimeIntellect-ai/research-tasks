You are acting as a systems programmer stepping into a broken C project. You've been handed the `librest_parser` project, a custom C library that implements a state machine to parse REST API requests into a custom data structure. 

Currently, the project is failing to compile due to linking errors, and the previous developer mentioned there are serious memory safety bugs (Undefined Behavior and memory leaks) when parsing malformed requests. Furthermore, there are no unit tests.

Your workspace is located at `/home/user/workspace/librest_parser`.

Here are your objectives:

1. **Fix the Linking Issues**: The project uses a `Makefile` to build a shared library `librest_parser.so` and an executable, but running `make` results in "multiple definition" linking errors. Identify and fix the root cause in the C header/source files.

2. **Fix Memory Safety and UB**: The custom string buffer (`src/string_buf.c`) and the state machine parser (`src/parser.c`) contain memory management bugs. Specifically, there is a use-after-free bug and a memory leak that occurs when a REST request parser encounters a syntax error. Fix the C code so that it is entirely memory-safe. Valgrind must report 0 errors and 0 leaks for any parsed input.

3. **Write a Test Suite**: Create a unit test file at `/home/user/workspace/librest_parser/tests/test_parser.c`. Write a `main` function that uses the library to parse the following three raw string inputs (representing REST requests):
   - Input 1 (Valid): `"GET /api/v1/users HTTP/1.1\r\nHost: localhost\r\n\r\n"`
   - Input 2 (Invalid Method): `"INVALID / HTTP/1.1\r\n\r\n"`
   - Input 3 (Malformed Header missing colon): `"POST / HTTP/1.1\r\nHost localhost\r\n\r\n"`

4. **Test Output**: Your `test_parser.c` should evaluate the parser's return codes. Input 1 should succeed (return 0). Input 2 and Input 3 should fail (return non-zero). 
   Compile your tests into an executable named `run_tests` in the workspace root. Run the tests and pipe the output to `/home/user/workspace/librest_parser/test_results.log`. 
   
   The log MUST contain exactly these lines (if successful):
   ```
   TEST 1: PASS
   TEST 2: PASS
   TEST 3: PASS
   ```

Ensure all your fixes are applied, the library builds via `make`, and `run_tests` runs completely clean under `valgrind --leak-check=full`.