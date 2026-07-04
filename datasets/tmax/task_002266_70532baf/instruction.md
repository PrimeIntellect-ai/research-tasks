You are tasked with investigating a statistical anomaly that was introduced into a data processing pipeline. 

You have been provided a Git repository at `/home/user/repo`. The repository contains a script `stats.py` and a module `calc.py`. At `HEAD`, the command `python stats.py` produces a calculated variance of `0.0` on the dataset `/home/user/data.txt`. We know that in an older version of the code (e.g., the initial commit), the variance was calculated accurately, but a regression was introduced somewhere in the 200 commits of the repository's history, causing a catastrophic cancellation error (floating-point precision loss).

Your objectives:
1. **Bisect the regression**: Use `git bisect` to find the exact commit hash that first introduced the variance calculation regression. The "good" commit is the very first commit in the repository.
2. **Reverse engineer the bad commit**: In the exact commit where the regression was introduced, the original author temporarily replaced `calc.py` with a compiled Python bytecode file (`calc.pyc`), hiding a hardcoded secret token inside it before replacing it back with source code in subsequent commits. Inspect the bytecode of this `.pyc` file at that specific commit to recover the value of the `SECRET_TOKEN` variable.
3. **Fix the floating-point anomaly**: At the current `HEAD` branch, fix the `get_variance(data)` function in `calc.py`. Modify it to use a numerically stable method (like Welford's algorithm or a standard two-pass algorithm) to avoid catastrophic cancellation. 
4. **Report the findings**: Run the fixed `stats.py` at `HEAD`. Create a file at `/home/user/result.json` with the following structure:
```json
{
  "bad_commit": "<full_40_char_commit_hash>",
  "secret_token": "<recovered_secret_string>",
  "fixed_variance": <float_value_of_corrected_variance>
}
```

Constraints:
* Do not change the overall structure of the `stats.py` script.
* Only modify `calc.py` at `HEAD` to fix the floating-point precision error.