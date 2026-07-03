You are a build engineer responsible for fixing, testing, and packaging a C++ mathematical evaluation tool. The tool previously failed in CI because tests passed individually but failed when run in a batch due to global state leakage between evaluations. 

Your goal is to implement the tool from scratch (to avoid the previous state-leakage bugs), write an end-to-end test orchestrator, and produce a final build artifact.

**Phase 1: Implementation (C++)**
Write a C++ program in `/home/user/math_eval/main.cpp` that builds to an executable named `calc_tool`. You must write a `Makefile` to compile it with `g++` (using C++17). 
The program should read from standard input line-by-line. Each line will contain a command followed by arguments:
1. `EVAL <rpn_expression>`: Evaluates a Reverse Polish Notation (RPN) mathematical expression. Supported operators are `+`, `-`, `*`, `/`. Operands are floating-point numbers.
2. `INTEGRATE <rpn_expression_with_x> <start> <end> <steps>`: Calculates the definite integral of the RPN expression over the range `[start, end]` using the standard **Trapezoidal Rule** with `steps` subintervals. The expression will contain the variable `x` and standard RPN operators.

For both commands, output the result on a new line, formatted to exactly 4 decimal places. Ensure absolutely no state leaks between line evaluations.

**Phase 2: End-to-End Test Orchestration**
Write a bash script at `/home/user/math_eval/run_tests.sh` that performs the following steps:
1. Cleans any previous builds and runs `make` to build `calc_tool`.
2. Generates an input file named `test_input.txt` with the following test cases exactly:
   - `EVAL 15 5 / 2 *`
   - `INTEGRATE x x * 0 10 1000`
   - `INTEGRATE x 2 * 3 + 0 5 50`
   - `EVAL 100 20.5 - 2 /`
3. Pipes `test_input.txt` into `./calc_tool` and saves the output to `test_output.txt`.
4. Packages the compiled `calc_tool` binary and `test_output.txt` into a compressed tarball named `/home/user/artifact.tar.gz`.

**Phase 3: Execution**
Run your `run_tests.sh` script to produce the final `/home/user/artifact.tar.gz` artifact. Leave the artifact in the `/home/user` directory.