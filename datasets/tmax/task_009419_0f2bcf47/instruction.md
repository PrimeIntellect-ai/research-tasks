You have been given access to a local Git repository at `/home/user/math_calc`. This project builds a C++ program that computes a mathematical sequence (specifically, the sum of squares up to N-1). 

Recently, a regression was introduced. The program correctly computes the result for small inputs, but for large inputs like `./calc 1000000`, it produces an incorrect result due to an integer overflow issue. 

We know that `HEAD~150` produces the correct output, but `HEAD` is broken.

Your tasks are as follows:

1. **Regression Bisection**: Use Git to bisect the history and find the exact commit that introduced the mathematical bug for `./calc 1000000`. 
   *Note*: A few commits in the middle of the history contain a missing `#include` which causes build failures. You must handle or skip these unbuildable commits during your bisection to accurately identify the first commit that successfully builds but produces the *wrong* mathematical result.
   Write the full Git commit hash of the first bad commit to `/home/user/bad_commit.txt`.

2. **Code Fix**: Fix the bug in the latest version (`HEAD`) of `src/calc.cpp`. The formula implementation has a flaw causing signed integer overflow before the assignment. Fix the code so it computes the correct value without overflowing. Compile the code using the provided `Makefile`, run `./calc 1000000`, and save the exact standard output to `/home/user/result.txt`.

3. **Secret Recovery**: A developer accidentally committed an API key (in the format `API_KEY=XYZ...`) in one of the past commits and later removed it. Analyze the Git history diffs to recover this API key. Write the value of the API key (just the value, not the `API_KEY=` part) to `/home/user/secret.txt`.

Requirements:
- Ensure all output files are placed exactly at `/home/user/bad_commit.txt`, `/home/user/result.txt`, and `/home/user/secret.txt`.
- No extra text or trailing newlines should be in `bad_commit.txt` and `secret.txt` other than the requested values.