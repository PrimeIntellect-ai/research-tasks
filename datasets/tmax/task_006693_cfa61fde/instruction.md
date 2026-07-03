You are tasked with finding a mathematical regression in a Bash script using `git bisect`. 

In `/home/user/repo`, there is a Git repository containing a script named `calc.sh`. This script is supposed to take a single integer `N` as an argument and calculate the sum of all integers from 1 to `N`. 

Recently, a bug was introduced that causes the script to fail or produce incorrect results for certain values of `N` (for example, `N=15`). We know that the tag `v1.0` represents a good, working state, and the tag `v2.0` (which is also the current `HEAD`) is broken.

Your task is to identify the exact commit that introduced the regression. 

Be aware:
1. Some intermediate commits contain syntax errors (a "build failure" equivalent in Bash) causing the script to be entirely unrunnable. You must skip these un-testable commits during your bisection rather than marking them as good or bad.
2. The mathematical bug might be related to how Bash evaluates numbers in arithmetic contexts. 

Once you have identified the first bad commit that introduced the mathematical bug, write its full 40-character commit hash to `/home/user/bad_commit.txt`.