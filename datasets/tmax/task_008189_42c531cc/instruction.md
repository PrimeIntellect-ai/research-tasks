You are a systems programmer brought in to debug a hybrid Python/C project that evaluates mathematical expressions. The project relies on a C extension for fast expression parsing, but the build is failing, the C library crashes, and the test suite cannot be completed. 

Here is the current state of the system in `/home/user/project`:
1. `expr_eval.c`: A C library that parses and evaluates basic math expressions (like "5+3", "10-2"). 
2. `libcalc.so`: A pre-compiled shared library that the project also depends on.
3. `input.txt`: A file containing a list of math expressions, one per line.
4. `baseline.txt`: A file containing expected sorted integer results, one per line.

Your tasks are:

**Phase 1: Fix Memory Safety and Linking Issues in C**
Examine `/home/user/project/expr_eval.c`. It has two major issues:
1. **Memory Corruption:** There is a bug in how memory is allocated for the results array, leading to undefined behavior or segmentation faults when handling multiple expressions. Fix the allocation logic.
2. **Symbol Conflict (Linking):** The `expr_eval.c` library defines a global helper function called `parse_op`. Unfortunately, `libcalc.so` also exports a `parse_op` symbol. When Python loads both libraries, this causes a symbol clash (similar to a peer dependency conflict). Modify `expr_eval.c` to encapsulate its helper so it does not conflict globally, while keeping its main `evaluate_expressions` function accessible.
Once fixed, compile `expr_eval.c` into a shared library named `libexpr_eval.so` in the `/home/user/project/` directory.

**Phase 2: Python FFI and Expression Evaluation**
Create a Python script at `/home/user/project/run_test.py`. This script must:
1. Use the `ctypes` module to load BOTH `/home/user/project/libcalc.so` and your compiled `/home/user/project/libexpr_eval.so`. 
2. Read the expressions from `/home/user/project/input.txt`.
3. Pass the array of expression strings to the `evaluate_expressions` C function. Make sure to define `argtypes` and `restype` correctly (it returns a pointer to an integer array).
4. Extract the evaluated integer results from the C pointer.
5. Sort the resulting integers in ascending order.

**Phase 3: Diffing and Testing**
Finally, your Python script (`run_test.py`) must:
1. Compare the sorted integer array against the contents of `/home/user/project/baseline.txt` (which contains one integer per line).
2. Generate a unified diff of the two lists of integers (as strings). Use Python's `difflib.unified_diff`. The baseline should be treated as the "from" file (named `baseline`) and your sorted results as the "to" file (named `results`).
3. Write the exact string output of the unified diff to `/home/user/project/diff.log`.
4. Free the memory allocated by the C library by calling the `free_results` function provided in `expr_eval.c` via ctypes.

All tasks must be completed using commands in the terminal. Once `run_test.py` is written, execute it to generate `diff.log`.