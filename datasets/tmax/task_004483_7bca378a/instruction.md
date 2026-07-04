You are an open-source maintainer reviewing a broken pull request for a new mathematical constraint satisfaction module. The PR is located in `/home/user/pr_review/`.

The contributor attempted to write a fast 3x3 Magic Square solver (digits 1-9, no repeats, all rows, columns, and both diagonals must sum to 15). The PR uses a custom `Square` data structure and an optimized x86_64 assembly routine to calculate sums. 

However, the PR is broken in two ways:
1. **Build System & Linking:** The `Makefile` fails to assemble and link the provided assembly file `fast_sum.s`. The C++ code relies on an `extern "C" int fast_sum(int a, int b, int c);` function defined in that assembly file.
2. **Constraint Logic:** The backtracking solver in `magic_square.cpp` has a bug. It correctly checks rows, columns, and the main diagonal, but the contributor forgot to enforce the constraint on the *anti-diagonal* (top-right to bottom-left). This causes it to output invalid squares.

Your task:
1. Fix the `Makefile` so that running `make` correctly assembles `fast_sum.s` and links it with `magic_square.cpp` to produce an executable named `magic_square`.
2. Fix the constraint logic in `magic_square.cpp` to correctly check the anti-diagonal using the `fast_sum` function.
3. Build the program using `make`.
4. Run the program and redirect its standard output to `/home/user/pr_review/solution.txt`.

The output written to `/home/user/pr_review/solution.txt` must consist of exactly 3 lines, each containing 3 space-separated integers representing the first valid magic square found by the solver.