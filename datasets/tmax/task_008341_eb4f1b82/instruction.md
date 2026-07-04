You are an engineer tasked with porting a mathematical evaluation tool to work in a minimal container environment. The tool is a hybrid Python/C application where the core mathematical expression parser and evaluator is written in C for performance, and Python is used for orchestration and data integrity verification.

Currently, the C core has memory safety issues (undefined behavior and memory leaks) that cause it to crash or leak memory when processing long expressions. 

Your objectives are:

1. **Fix the C code:**
   The C source file is located at `/home/user/evaluator.c`. It contains a function `double evaluate_postfix(const char* expr)` that evaluates space-separated postfix mathematical expressions (supporting `+` and `*` operations). 
   Identify and fix the memory safety issues (specifically, a buffer allocation error and a memory leak).

2. **Write the Orchestrator (`/home/user/orchestrator.py`):**
   Create a Python script that performs the following end-to-end tasks:
   a. **Polyglot Build:** Programmatically compile `/home/user/evaluator.c` into a shared library `libeval.so` in `/home/user/` using `gcc`.
   b. **Checksum Calculation:** Implement a Python function to compute a simple checksum for each expression string. The checksum algorithm is the sum of the ASCII values of all characters in the string, modulo 256.
   c. **C Binding:** Use Python's `ctypes` module to load `libeval.so` and call `evaluate_postfix`.
   d. **Evaluation and Output:** Read a list of expressions (one per line) from `/home/user/input.txt`. For each expression, compute its checksum and use the C library to compute its result.
   e. Write the results to `/home/user/output.json` in the following exact format:
   ```json
   {
     "expression_string": {
       "checksum": 123,
       "result": 45.0
     }
   }
   ```
   (Do not include newline characters from the input lines in the `expression_string` keys or checksum calculations).

Ensure your script runs cleanly and produces the correct `/home/user/output.json`.