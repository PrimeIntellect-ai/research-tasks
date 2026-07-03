You are acting as a release manager preparing a deployment for a hybrid C/Python project. The project consists of a C library that performs high-speed expression evaluation and a Python wrapper that exposes it. However, the build is currently broken, there is a bug in the C logic, and we lack rigorous property-based testing. 

Your tasks are to fix the C library, make it build correctly, write an expression parser, and write property-based tests.

Here is the setup:
The project is located in `/home/user/project`.

1. **Fix the Makefile and C code**:
   - The C code is in `/home/user/project/c_src/libevaluator.c`. It has a mathematical bug in the multiplication operation. Fix it.
   - The Makefile in `/home/user/project/c_src/Makefile` is broken. It is trying to build a shared library (`libevaluator.so`) but forgets the necessary flags (`-fPIC` during compilation and `-shared` during linking). Fix the Makefile so that running `make` in that directory successfully produces `/home/user/project/c_src/libevaluator.so`.
   - Run `make` to build the library.

2. **Write the Parser**:
   - The Python wrapper `/home/user/project/eval_wrapper.py` is already written and loads `libevaluator.so`. It provides a function `evaluate_op(op_code, a, b)` where `op_code` is 0 (ADD), 1 (SUB), 2 (MUL), or 3 (DIV).
   - Write a Python script `/home/user/project/parser.py` that reads `/home/user/project/expressions.txt`.
   - Each line in `expressions.txt` contains an operation and two integers, separated by spaces (e.g., `ADD 10 20`, `MUL 6 7`).
   - For each line, parse the text, map the string operation to the correct integer `op_code`, and call `evaluate_op(op_code, a, b)` from `eval_wrapper.py`.
   - Write the integer result of each evaluation to `/home/user/project/results.txt`, one result per line, in the same order as the input file.

3. **Property-Based Testing**:
   - Write a property-based test script in `/home/user/project/test_eval.py` using `pytest` and `hypothesis`.
   - You must test `evaluate_op` from `eval_wrapper.py` against standard Python math for all 4 operations (ADD, SUB, MUL, DIV).
   - Use `hypothesis.given` with `st.integers()`. Constrain the integers to be between -1000 and 1000.
   - For DIV, ensure you handle division by zero (the C code returns 0 when `b == 0`, so your test should expect that behavior).
   - The tests must pass successfully when running `pytest /home/user/project/test_eval.py`.

Make sure all files are saved and tests pass before you finish.