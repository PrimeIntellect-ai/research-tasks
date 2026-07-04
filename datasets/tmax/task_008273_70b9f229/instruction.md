You are an engineer tasked with diagnosing and fixing a severe regression in a Rust application. 

The application is located in `/home/user/collatz-calc`. It calculates the number of steps required to reach `1` for a given positive integer, following a specific mathematical sequence.

Recently, the production service started experiencing intermittent timeouts. We have extracted the recent logs from the container and saved them to `/home/user/container.log`. The logs indicate that the process hangs indefinitely for certain specific input values, causing a timeout.

Your task:
1. **Container Log Inspection:** Analyze `/home/user/container.log` to identify the specific input value that intermittently causes the application to hang.
2. **Regression Bisection:** The bug was introduced somewhere in the last 200 commits. Use Git bisection to pinpoint the exact commit that introduced the infinite loop for the failing input.
3. **Record Findings:** Once you find the offending commit, save its full 40-character Git hash to `/home/user/bad_commit.txt`.
4. **Formula Correction & Loop Termination Fix:** The regression was caused by a subtle, flawed modification to the core mathematical formula, resulting in an infinite loop instead of sequence termination. On the `main` branch (the latest commit), correct the formula in `src/main.rs` to its original, mathematically sound state so that the loop terminates correctly for all positive integers.
5. **Verification:** Ensure your fixed code compiles and runs successfully using `cargo run -- <failing_input>`.

Constraints:
- Do not modify the repository's git history (no `git rebase`, `git reset`, or `git commit`). Just leave the corrected file in the working directory on the `main` branch.
- Ensure the result in `bad_commit.txt` has no leading or trailing whitespace.