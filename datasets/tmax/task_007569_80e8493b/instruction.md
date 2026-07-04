You are tasked with bisecting a regression in a Bash project and recovering a lost secret. 

A developer has a Git repository located at `/home/user/repo`. The current `main` branch (`HEAD`) has a regression: the script `calc_convergence.sh` enters an infinite loop and fails to converge when executed (e.g., running `./calc_convergence.sh 25` hangs instead of outputting `5`). 

We know that the commit tagged `v1.0` (which is about 200 commits ago) is perfectly fine and works correctly. 

Your tasks are:
1. **Bisect the regression**: Use `git bisect` to find the exact commit that introduced the infinite loop. Since the bad commit hangs, you will likely need to write a small test script wrapping the execution in a `timeout` to automate the bisect.
2. **Identify the Bad Commit**: Once you have found the first bad commit, write its full SHA-1 hash to `/home/user/bad_commit.txt`.
3. **Recover a Secret**: In that exact same bad commit, the developer accidentally pasted an API key in the comments of `calc_convergence.sh`. They deleted the secret in the very next commit. Find this API key (it looks like `SECRET_KEY="<string>"`) from the bad commit's diff or tree, and write just the `<string>` value to `/home/user/secret.txt`.
4. **Fix the Loop Termination**: Go back to the `main` branch (`git checkout main`). Inspect `calc_convergence.sh`. The script implements an integer square root using a convergence algorithm, but the loop termination condition or variable update is flawed, causing the infinite loop. Fix the Bash code so that it converges correctly and terminates. Save your corrected version of the script to `/home/user/fixed_calc.sh`.

Ensure that:
- `/home/user/fixed_calc.sh` has executable permissions.
- Running `/home/user/fixed_calc.sh 100` outputs `10` and exits immediately.
- `/home/user/secret.txt` contains only the recovered secret string (no quotes or variable names).