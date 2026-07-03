You are a script developer working on a new mathematical utility toolchain. You have been handed an incomplete project in `/home/user/matheval` that builds a Reverse Polish Notation (RPN) evaluation library in C, alongside a test suite and a planned Python CLI.

Unfortunately, the previous developer left the project in a broken state:
1. The project cannot compile. There is a CMake configuration issue causing a link-time error where the test executable cannot find the shared library.
2. Even if it compiles, the tests fail. The evaluator in `src/eval.c` contains logical bugs related to order-dependent operations (subtraction and division).
3. The polyglot integration is incomplete. There is no Python wrapper to use the C library.

Your task is to fix and complete the project:

1. **Fix the Build**: Modify `/home/user/matheval/CMakeLists.txt` so that the project successfully configures and compiles inside a `build` directory (`/home/user/matheval/build`). Ensure `ctest` can execute successfully. Note: The project enforces `CMAKE_SKIP_BUILD_RPATH TRUE`. You may remove this or find another way to ensure the test executable finds the shared library at runtime.
2. **Fix the C Code**: Correct the RPN evaluation logic in `/home/user/matheval/src/eval.c`. 
3. **Write an Integration Test**: Create a Python script at `/home/user/matheval/integration_test.py` that uses the `ctypes` module to load the compiled `libmatheval.so` from the `build` directory. 
   - Use the loaded C function to evaluate the RPN expression: `"15 7 1 1 + - / 3 * 2 1 1 + + -"`
   - The Python script must write the final evaluated result (as a float string, e.g., `5.0`) directly to `/home/user/matheval/integration_result.log`.

Ensure that after your work is done:
- `cd /home/user/matheval/build && make` builds successfully.
- `cd /home/user/matheval/build && ctest` reports 100% tests passed.
- Running `python3 /home/user/matheval/integration_test.py` successfully creates the log file with the correct mathematical result.