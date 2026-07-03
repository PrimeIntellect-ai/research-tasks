You are tasked with debugging a regression in a numerical simulation project. 

The repository is located at `/home/user/sim_repo`. The project consists of a C program (`sim.c`) that calculates a mathematical root using an iterative convergence method. 

At the tag `v1.0`, the program compiled correctly and successfully converged to the correct value (returning a `0` exit code). However, a regression was introduced somewhere in the subsequent 200 commits. Currently, at `HEAD`, the program fails to converge and exits with a non-zero exit status.

Your task:
1. Navigate to `/home/user/sim_repo`.
2. Find the exact commit that introduced the convergence failure. You are encouraged to use `git bisect` and write a small test script to automate the process (e.g., compiling `sim.c` with `gcc sim.c -lm` and checking its exit code).
3. Once you have identified the first bad commit, save its full 40-character Git commit hash to a file named `/home/user/bad_commit_hash.txt`.

Do not modify the Git history. Only write the exact commit hash to the file.