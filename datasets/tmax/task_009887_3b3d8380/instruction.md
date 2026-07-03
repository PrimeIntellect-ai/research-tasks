You are tasked with fixing and orchestrating tests for a mathematical graph interpreter written in C. 

The project, located at `/home/user/calcgraph`, is a simple interpreter that reads a custom mathematical dependency language ("CalcGraph") and computes the final value of a specific target node by evaluating a Directed Acyclic Graph (DAG) of mathematical operations.

Currently, the project fails to compile, has a critical bug in its evaluation logic, and lacks an end-to-end test runner.

Your objectives are:

1. **Fix the Build**:
   The `Makefile` in `/home/user/calcgraph` is configured with `-Werror` but currently fails to compile and link. Fix the missing includes, compiler errors, and linker errors so that running `make` successfully produces the `calcgraph` executable.

2. **Fix the Graph Evaluator**:
   There is a logical error in `/home/user/calcgraph/eval.c`. The graph traversal is supposed to evaluate operations (ADD, MUL, SUB) based on child node dependencies. However, it currently produces incorrect mathematical results for multiplication operations due to a logic flaw in the emulator core. Find and fix this bug.

3. **End-to-End Test Orchestration**:
   Create a bash script at `/home/user/calcgraph/run_tests.sh` that does the following:
   - Compiles the code (`make clean && make`).
   - Runs the interpreter on three provided test files in the `/home/user/calcgraph/tests/` directory: `test1.cg`, `test2.cg`, and `test3.cg`.
   - The CLI usage is `./calcgraph <filepath>`.
   - Captures the standard output of each run (which prints a single integer representing the root node's evaluated result).
   - Writes the results to `/home/user/results.log` in the exact following format:
     ```
     test1: <result>
     test2: <result>
     test3: <result>
     ```

**Important Constraints:**
- Do not change the CLI arguments of the `calcgraph` program.
- `/home/user/results.log` must contain exactly three lines, formatted exactly as shown above.
- Make sure `run_tests.sh` has executable permissions.