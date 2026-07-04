You are tasked with debugging a mathematical regression in a Bash-based project. 

A project located at `/home/user/math_repo` contains a script `calc_integral.sh` that calculates the definite integral of $f(x) = 3x^2$ from $x=0$ to $x=10$ using the trapezoidal rule over 1000 steps. The correct mathematical result should be extremely close to `1000.0000` (the analytical area).

However, a regression was introduced somewhere in the repository's recent history. The `main` branch currently outputs an incorrect mathematical result. The repository has roughly 200 commits. The tag `v1.0` points to an older commit that is known to be perfectly completely mathematically correct.

Your task:
1. Use `git bisect` (and optionally write a delta debugging/minimization test script to automate it via `git bisect run`) to identify the exact commit that introduced the mathematical bug.
2. Once you find the bad commit, write its exact commit message (just the message, no hash or author details) to `/home/user/bad_commit_message.txt`.
3. Analyze the compiler/interpreter output or use bash debugging (`bash -x`) to understand what mathematical formula implementation was corrupted.
4. Fix the formula in `calc_integral.sh` on the `main` branch so that it correctly computes the area using the trapezoidal rule.
5. Run the fixed script and redirect its standard output to `/home/user/fixed_area.txt`.

Ensure all files are created exactly at the specified absolute paths.