You have just inherited an unfamiliar codebase located at `/home/user/math-solver`. It is a Go library that provides iterative mathematical solvers.

Recently, the main branch started failing its CI tests. The previous maintainer mentioned that a commit was merged recently that supposedly "optimized" the memory usage of some internal variables, but ever since then, the `FindRoot` function in `solver.go` has been experiencing a convergence failure.

Your task is to:
1. Navigate to `/home/user/math-solver`.
2. Use `git bisect` to find the exact commit that introduced the regression. The last known good commit is tagged as `v1.0`. The current `HEAD` (on the `main` branch) is known to be broken.
3. Once you identify the broken commit, diagnose the issue. You will find that an improper cast to a lower precision floating-point type is causing catastrophic loss of precision, leading the iterative algorithm to fail to converge within the allowed iterations and return `NaN`.
4. Fix the precision bug in `solver.go` so that the algorithm correctly converges again using `float64` for all intermediate calculations.
5. The `solver_test.go` file contains several tests. Apply delta debugging/test minimization: remove all test functions from `solver_test.go` *except* `TestFindRoot`. Ensure the remaining test successfully passes.
6. Create a file at `/home/user/resolution.txt` containing exactly two lines:
   - Line 1: The full 40-character Git commit hash of the commit that introduced the bug.
   - Line 2: The successfully computed root from `FindRoot(2.0, 1e-9)`, rounded to exactly 6 decimal places (e.g., `1.234567`).

Do not change the method signature of `FindRoot` or the mathematical logic of the algorithm itself, only fix the data types/precision issue that was introduced.