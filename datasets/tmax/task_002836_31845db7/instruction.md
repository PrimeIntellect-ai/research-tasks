You are an open-source maintainer reviewing a Pull Request for `libastmath`, a lightweight C library used for evaluating Reverse Polish Notation (RPN) mathematical expressions.

The PR attempts to add support for a new exponentiation operator (`^`), improve cross-compilation for an embedded target, and refactor memory management. However, the CI pipeline is failing, and the PR author has abandoned the branch. 

You need to step in and fix the following issues in the project located at `/home/user/libastmath`:

1. **Conditional Build Failure**: The Makefile is configured to support a generic build and an embedded build. When compiling with `make target=embedded`, the build fails due to a bug in the conditional compilation blocks (`#ifdef`) inside `eval.c`.
2. **Mathematical Evaluation Bug**: The newly added `^` (power) operator parses correctly but yields completely incorrect mathematical results. You need to fix the evaluation logic so it correctly calculates powers (e.g., $2^3 = 8$). Note: you might need to update the build system to link the correct standard libraries if you use standard mathematical functions.
3. **Memory Leak**: The expression parser creates Abstract Syntax Tree (AST) nodes, but the CI pipeline's memory profiler reports a memory leak when evaluating expressions. You must debug and fix the memory leak in the AST cleanup logic.

**Requirements & Verification:**
- Fix the C source code and Makefile in `/home/user/libastmath`.
- The generic build (`make`) must produce `./astmath`.
- The embedded build (`make target=embedded`) must compile successfully and produce `./astmath_embedded`.
- Evaluate the expression `"2 3 2 ^ ^"` (which mathematically represents $2^{(3^2)}$) using `./astmath` and redirect the standard output to `/home/user/math_result.txt`.
- Run `valgrind --leak-check=full ./astmath "4 5 + 2 *"` and save the stderr output of Valgrind to `/home/user/valgrind_report.txt`. The report must show `0 bytes in 0 blocks` definitely lost.