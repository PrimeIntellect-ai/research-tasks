We are in the process of rewriting our legacy C++ optimization engine in Python. The legacy engine is available as a stripped binary at `/app/oracle_engine`. 

Recently, we discovered that our new Python implementation, located in the git repository at `/home/user/py_engine`, is experiencing convergence failures and precision loss on edge cases. 

The Python implementation was fully matching the oracle at tag `v1.0` (known good), but is failing at tag `v2.0` (current HEAD, known bad). There are exactly 200 commits between `v1.0` and `v2.0`. 

Your objectives are:
1. Understand the I/O format of `/app/oracle_engine`. It takes a CSV file containing an initial vector and adjacency matrix, and outputs the converged state vector.
2. Write a testing wrapper to compare the output of the Python engine (`python /home/user/py_engine/solver.py <input_csv>`) against the oracle.
3. Use `git bisect` across the commit history to identify the exact commit that introduced the floating-point / convergence regression.
4. Analyze the diff of the bad commit, understand the floating-point truncation or convergence early-stopping bug, and repair the Python codebase at `HEAD` (`v2.0`).
5. Run your repaired Python engine on the evaluation dataset located at `/home/user/eval_data.csv`.
6. Save the final output to `/home/user/predictions.csv`. The output format must be a single column of floating-point numbers, one per line.

Do not attempt to reverse-engineer the exact C++ source of the oracle; treat it as a black box that yields the ground-truth converged floating-point arrays. Your goal is to fix the Python implementation so it converges correctly.