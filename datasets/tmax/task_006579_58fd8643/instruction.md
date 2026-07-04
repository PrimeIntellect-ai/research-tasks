You are a QA engineer tasked with fixing a broken build for a polyglot mathematical application and creating a property-based testing script to verify its correctness.

The application computes the Greatest Common Divisor (GCD) of two integers. It consists of a high-performance C backend and a Python wrapper, located in `/home/user/app/`. 

However, the provided build script (`/home/user/app/build.sh`) is currently broken and fails to compile the C code and set up the Python environment properly.

Your task has two parts:

Part 1: Fix the Build
1. Inspect and fix `/home/user/app/build.sh`. It should compile `gcd.c` into an executable named `gcd_calc` in the same directory, and ensure `math_wrapper.py` is ready to use. 
2. Execute the fixed `build.sh`.

Part 2: Property-Based Testing in Bash
Write a Bash script at `/home/user/app/prop_test.sh` that performs property-based testing on the Python wrapper. 
The Python wrapper is called like this: `python3 math_wrapper.py <a> <b>` and it prints a single integer (the GCD).

Your script `prop_test.sh` must:
1. Generate 100 random pairs of integers `(a, b)`, where both `a` and `b` are randomly chosen between 1 and 1000 (inclusive).
2. For each pair, call the wrapper to compute `g = python3 math_wrapper.py a b`.
3. Verify the following three mathematical properties for every pair:
   - Divisibility A: `a` modulo `g` must equal 0.
   - Divisibility B: `b` modulo `g` must equal 0.
   - Symmetry: `python3 math_wrapper.py a b` must exactly equal `python3 math_wrapper.py b a`.
4. If any property fails for any pair, write "PROPERTY TEST FAILED" to `/home/user/app/test_report.log` and exit immediately.
5. If all 100 iterations pass successfully, write exactly "ALL PROPERTIES PASSED" to `/home/user/app/test_report.log`.

Make sure you run your `prop_test.sh` script to generate the final log file.