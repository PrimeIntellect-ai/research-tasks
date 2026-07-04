You are provided with a Git repository at `/home/user/math_parser`. The repository contains a Bash script `calc.sh` that parses and evaluates simple prefix mathematical expressions (e.g., `./calc.sh ADD 5 10`).

Recently, a regression was introduced somewhere in the last 200 commits (after the `v1.0` tag). The script now fails or produces incorrect results for certain format parsing edge cases.

Your tasks are:
1. Write a fuzzing script to compare the output of the current `master` branch with the `v1.0` tag. Find a combination of valid operations (`ADD`, `SUB`, `MUL`, `DIV`) and integer arguments (between -10 and 10) that triggers the bug.
2. Use `git bisect` to identify the exact commit hash that introduced the regression. Save this full 40-character commit hash to `/home/user/bug_commit.txt`.
3. Fix the format parsing edge case in `calc.sh` at the HEAD of the `master` branch so that it correctly handles all valid integer inputs (including negatives) while still rejecting invalid non-integer formats. The fixed script should be saved at `/home/user/math_parser/calc.sh`.

Ensure that `/home/user/bug_commit.txt` contains exactly the commit hash and a newline, and that `calc.sh` functions correctly for all valid inputs at the end of your process.