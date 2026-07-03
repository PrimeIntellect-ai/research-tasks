You are tasked with migrating a legacy Python 2 mathematical expression interpreter to Python 3. The legacy system parses and evaluates prefix-notation mathematical expressions, and calculates a checksum of the expression using a C library via Foreign Function Interface (FFI). 

The legacy files are located in `/home/user/legacy/`:
- `/home/user/legacy/libchecksum.so`: A compiled C shared library.
- `/home/user/legacy/math_eval.py`: The Python 2 interpreter script.

Your objectives:
1. **Port the Code**: Copy the script to `/home/user/modern/math_eval.py` and upgrade it to Python 3.
   - You must fix any Python 2 specific syntax (e.g., `print` statements, `xrange`).
   - You must fix the `ctypes` FFI bindings. The C library function `compute_checksum` expects a null-terminated C string (`char*`). In Python 3, passing standard strings to `c_char_p` directly will fail; you must ensure the expression string is correctly encoded to UTF-8 bytes before passing it to the C function.
   - **Crucial mathematical constraint**: The legacy Python 2 interpreter used standard division `/` on integers, which performed floor division. Your Python 3 port MUST preserve this exact mathematical behavior (i.e., evaluate division as integer floor division).

2. **Process Inputs**:
   There is an input file at `/home/user/inputs.txt` containing one prefix mathematical expression per line.
   Create a script or modify `math_eval.py` so that when run, it reads `/home/user/inputs.txt`, evaluates each expression and its checksum, and writes the results to `/home/user/output.txt`. 
   The output format for each line in `/home/user/output.txt` must exactly be:
   `Expression: <original_string> | Result: <math_result> | Checksum: <checksum_value>`

3. **Create a Test Fixture**:
   Create a Python 3 test file at `/home/user/modern/test_math.py` using the standard `unittest` and `unittest.mock` libraries.
   - It must import your ported `math_eval` module.
   - It must contain a test class with at least one test method.
   - Use `mock.patch` to mock the FFI call to the C library (`compute_checksum`) so that it always returns the integer `999`.
   - The test must assert that when `math_eval.evaluate_and_hash("- 10 3")` is called, the returned result is exactly the tuple `(7, 999)`.

**Constraints**:
- Use Python 3.x for all new code.
- Do not modify or recompile `/home/user/legacy/libchecksum.so`. Load it dynamically in your Python 3 code using its absolute path (`/home/user/legacy/libchecksum.so`).
- Make sure to correctly handle strings vs bytes in the FFI boundary.