You have just joined a team and inherited an unfamiliar legacy codebase at `/home/user/solver_repo`. 

The repository wraps a proprietary, highly-optimized stripped binary located at `/app/root_finder`. This binary performs Newton-Raphson iterative root-finding for cubic polynomials. It expects inputs in the form of coefficients and an initial guess.

Recently, the system has experienced severe reliability issues. There are two parts to your assignment:

1. **Regression Diagnosis (Git Bisection & Convergence Repair):**
   A recent commit in the repository broke the Python wrapper's ability to handle convergence bounds properly. Specifically, the wrapper (`wrapper.py`) is failing on valid but slow-converging edge cases (there is a test script `test_edge.py` in the repo that currently fails but used to pass).
   - Use `git bisect` to find the exact commit hash that introduced the bug.
   - Write the full 40-character commit hash to `/home/user/bad_commit.txt`.
   - Fix the logic in `wrapper.py` so that `test_edge.py` passes once again.

2. **Corrupted Input Handling (Adversarial Filter):**
   The `/app/root_finder` binary is fragile. If provided with "evil" inputs (e.g., initial guesses where the derivative is exactly zero, causing a division by zero, or malformed data causing the Newton method to diverge into oscillatory loops or segfaults), it crashes the entire pipeline.
   - You must write a robust Python script at `/home/user/solver_repo/filter.py` that acts as a gatekeeper.
   - The script will be invoked as: `python3 /home/user/solver_repo/filter.py <path_to_input.csv>`
   - The CSV file contains a single line: `a,b,c,d,x0` representing the polynomial $f(x) = ax^3 + bx^2 + cx + d$ and the initial guess $x_0$.
   - Your `filter.py` must perform mathematical and structural validation. 
   - If the input is well-behaved ("clean") and will converge safely, your script MUST exit with code `0`.
   - If the input is corrupted, malformed, or mathematically degenerate (e.g., $f'(x_0) \approx 0$, which diverges the Newton-Raphson solver), your script MUST exit with code `1`.

We have provided two sample directories for you to test your filter:
- `/home/user/corpora/clean/` contains valid CSVs.
- `/home/user/corpora/evil/` contains malformed or mathematically degenerate CSVs.

The automated verification system will test your `filter.py` against a hidden, extended set of clean and evil corpora. Your filter must perfectly distinguish between them.