You are a mobile build engineer maintaining a cross-platform CI/CD pipeline. Part of our pipeline calculates a "Build Complexity Score" for dynamic build matrix generation. This score is calculated using an evaluator written in Go, which relies on a highly optimized C library for platform-specific hardware heuristics.

Currently, the pipeline is broken. The C library's Makefile is incorrectly configured and fails to build, and the Go evaluation tool hasn't been implemented yet. 

Your task is to fix the build system, write the expression evaluator in Go, and write a test fixture for it.

**Phase 1: Fix the C Library Build System**
In `/home/user/clib`, you will find `hwscore.c`, `hwscore.h`, and a `Makefile`. The C code uses inline assembly to perform a fast heuristic calculation.
1. The `Makefile` is broken (syntax errors, missing position-independent code flags, missing shared library flags). 
2. Fix the `Makefile` so that running `make` successfully compiles `hwscore.c` into a shared library named `libhwscore.so` in the `/home/user/clib` directory.

**Phase 2: Write the Go Expression Evaluator**
Write a Go program at `/home/user/pipeline.go` that acts as the pipeline tool.
1. The tool must read `/home/user/rules.txt`. Each line in this file contains a mathematical expression in Reverse Polish Notation (RPN).
2. The tokens in the RPN expressions are separated by single spaces. The valid tokens are:
   - Positive integers
   - The operators: `+`, `-`, `*`, `/` (integer division)
   - The special token `HW`.
3. When the Go program evaluates a line and encounters the `HW` token, it must calculate the hardware score for that specific line by calling the C function `int get_hw_score(int seed)` from `libhwscore.so` via CGO. The `seed` passed to the function must be the 1-indexed line number of the file (e.g., the first line has seed=1, the second line has seed=2).
4. The Go program should evaluate every line in `/home/user/rules.txt` and write the final integer result of each line to `/home/user/eval_results.txt`, with one integer per line corresponding to the input lines.

**Phase 3: Write Test Fixtures**
Create a test file `/home/user/pipeline_test.go` for your evaluation logic.
1. To ensure testability without CGO dependencies, the core RPN evaluation logic in your Go code must accept a dependency-injected function for handling the `HW` token, e.g., `EvaluateRPN(expr string, hwFunc func(int) int, seed int) int`.
2. Write at least two unit tests in `pipeline_test.go` that mock the `hwFunc` to return predictable integers and verify that the RPN parsing and arithmetic logic works correctly.
3. The tests should pass successfully when `go test pipeline_test.go pipeline.go` is executed.

**Constraints:**
- The Go program must be the `main` package and executable.
- Assume `rules.txt` contains valid RPN expressions with at least one operand/operator.
- Ensure your Go program appropriately sets `CGO_CFLAGS` and `CGO_LDFLAGS` to link against `/home/user/clib/libhwscore.so` (you may need to configure `LD_LIBRARY_PATH` or rpath for it to run).