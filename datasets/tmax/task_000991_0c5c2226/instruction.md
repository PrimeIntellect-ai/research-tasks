You are a developer working on a web security team. We recently had an incident where a vulnerable C-based mathematical expression evaluator (used in our web backend) caused a denial-of-service via memory corruption and unhandled division-by-zero panics. You need to organize our project files and rewrite the evaluator in safe Rust.

Your task has three phases:

**Phase 1: Project Organization**
1. An old legacy file exists at `/home/user/legacy.c`. Move it to `/home/user/math_eval/legacy/legacy.c`.
2. Initialize a new Rust binary project at `/home/user/math_eval/evaluator`.

**Phase 2: Safe Interpreter Implementation**
Write a safe Rust interpreter in `/home/user/math_eval/evaluator/src/main.rs`.
The interpreter must parse and evaluate nested mathematical functions provided as a single command-line argument. 
Supported functions:
- `add(a, b)`: Addition
- `sub(a, b)`: Subtraction
- `mul(a, b)`: Multiplication
- `div(a, b)`: Integer division (truncating)

Arguments `a` and `b` can be either integers or nested function calls.
Example input: `mul(add(2, 3), sub(10, 4))` should evaluate to `30`.

**Security constraints:**
- If the input is malformed, has invalid syntax, or attempts to divide by zero, the program MUST NOT panic. It must print exactly `EVAL_ERROR` to standard output and exit with code 0.
- Otherwise, it must print the integer result to standard output.

**Phase 3: Benchmarking and Integration**
We have a dataset of 1,000 generated expressions at `/home/user/dataset.txt` (one per line). 
Write a script (Bash or Python) or a Rust test at `/home/user/math_eval/benchmark.sh` that reads this file, runs your compiled Rust binary on each line, and sums up all the VALID numerical results (ignoring any `EVAL_ERROR` outputs). 
Write the final sum as a simple integer to the file `/home/user/benchmark_result.txt`.

Ensure your Rust code is compiled in release mode before running the benchmark.