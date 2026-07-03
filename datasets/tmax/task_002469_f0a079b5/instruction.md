I have a messy Python project in `/home/user/project` that implements a simple text-based interpreter for math commands. It relies on a C library for the actual operations (using `ctypes`). Currently, the project files are all dumped in the root directory, there is a circular dependency preventing the Python code from running, the C library isn't compiled, and the tests are incomplete.

I need you to act as a developer and organize the project files, fix the bugs, and get the test suite passing.

Here are your requirements:

1. **Directory Organization (Constraint Satisfaction):**
   Restructure `/home/user/project` to strictly match the following layout:
   - `/home/user/project/src/c_lib/`: Must contain `math_ops.c` and the compiled shared library.
   - `/home/user/project/src/pylib/`: Must contain `interpreter.py`.
   - `/home/user/project/tests/`: Must contain all test files (`test_interpreter.py`, `test_config.py`, and a new integration test).
   Remove any leftover files from the root `/home/user/project` (except the directories above and your output logs).

2. **C Compilation & FFI:**
   - Compile `math_ops.c` into a shared library named `libmath.so` inside `/home/user/project/src/c_lib/`.
   - Modify `interpreter.py` so that `ctypes` dynamically loads `libmath.so` based on the script's location (it should resolve the path to `../c_lib/libmath.so` relative to itself, rather than using a hardcoded absolute path).

3. **Fix Circular Dependency:**
   There is a circular import involving `interpreter.py` and `test_config.py` that prevents the module from loading. Refactor the imports to break this circular dependency without breaking the test suite's ability to import the interpreter.

4. **Testing:**
   - Write a new test file `/home/user/project/tests/test_integration.py` using `pytest`. It must test the `SUB` command by asserting that `evaluate("SUB 10 4")` returns `6`.
   - Ensure you have the `pytest` package installed.
   - Run the full test suite using `pytest /home/user/project/tests` and redirect the standard output to `/home/user/project/test_results.log`.

Your task is complete when the directory is cleanly organized, the C library is compiled, the circular import is fixed, the new test is written, and `/home/user/project/test_results.log` proves that all tests pass.