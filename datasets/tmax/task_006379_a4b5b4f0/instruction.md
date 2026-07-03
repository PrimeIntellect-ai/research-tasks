You are an open-source maintainer reviewing a pull request for a data processing pipeline. The PR introduces a C shared library (`libeval.so`) to parse and evaluate mathematical expressions quickly, and a Python script (`check_constraints.py`) that uses `ctypes` to call this library and filter data based on constraints.

However, the PR is currently broken:
1. The author forgot to configure the ABI correctly in Python. The C function `eval_expr` returns a `double`, but Python's `ctypes` defaults to expecting a 32-bit `int`. This causes the constraint satisfaction logic to operate on garbage memory values.
2. There is a memory leak in the C code. The PR author allocated memory for string manipulation during expression parsing but forgot to free it. 

Your task:
1. Inspect `/home/user/pr-review/check_constraints.py` and fix the ABI mismatch by specifying the correct `restype` and `argtypes` for the `eval_expr` function.
2. Inspect `/home/user/pr-review/evaluate.c` using a memory debugging tool (like `valgrind` or simply reading the code) and fix the memory leak.
3. Recompile the C shared library using:
   `gcc -shared -o /home/user/pr-review/libeval.so -fPIC /home/user/pr-review/evaluate.c`
4. Run the Python script on the input data:
   `python3 /home/user/pr-review/check_constraints.py /home/user/pr-review/data.txt > /home/user/pr-review/passed.txt`

The script will evaluate expressions like `5.5+4.5` and verify if they meet a threshold constraint. The final correctly filtered results must be written to `/home/user/pr-review/passed.txt`.