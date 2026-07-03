You are an engineer porting a legacy C-based data processing tool into a minimal Python container environment. 

The original tool evaluated simple mathematical expressions, but we are moving to a hybrid architecture where Python handles the file processing and parsing, while the legacy C code acts as the evaluation engine.

You have been provided with a directory `/home/user/project/` containing:
1. `/home/user/project/src/eval.c`: The legacy C engine containing an `int evaluate(const char* op, int a, int b)` function.
2. `/home/user/project/Makefile`: A build script meant to compile `eval.c` into a shared library `libeval.so`.
3. `/home/user/project/data.txt`: A dataset of expressions to process.

Your task consists of two parts:

**Part 1: Fix the Build System**
The provided `Makefile` is broken and fails to produce a valid shared library that Python can load. Modify `/home/user/project/Makefile` so that running `make` inside `/home/user/project/` successfully compiles `src/eval.c` into a dynamically linkable shared object named `libeval.so` in the `/home/user/project/` directory.

**Part 2: Implement the Python Processor**
Write a Python script at `/home/user/project/processor.py` that acts as the interpreter for our data file. The script must:
1. Load the compiled `libeval.so` shared library using Python's `ctypes` module.
2. Define the correct argument and return types for the C function `evaluate` (it takes a C-string and two integers, and returns an integer).
3. Read the file `/home/user/project/data.txt` line by line. Each line contains an expression in the format `OP ARG1 ARG2` (e.g., `ADD 10 5`).
4. Parse each line, invoke the C `evaluate` function with the parsed arguments, and write the results to `/home/user/project/output.log`.

The output in `/home/user/project/output.log` must be formatted exactly as follows for each line:
`Line [N]: [OP] [ARG1] [ARG2] = [RESULT]`
Where `[N]` is the 1-based line number.

For example, if `data.txt` contains:
```
ADD 15 25
MUL 4 7
```
The `/home/user/project/output.log` should contain exactly:
```
Line 1: ADD 15 25 = 40
Line 2: MUL 4 7 = 28
```

Ensure your Python script runs cleanly and generates the expected output log.