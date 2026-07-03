I need your help fixing a regression in our numerical optimization engine. The source code is in a Git repository located at `/home/user/optimization_engine`. 

Historically, this engine worked perfectly, as demonstrated by our legacy, stripped binary oracle located at `/app/oracle_bin`. However, a regression was introduced somewhere in the last 200 commits (between the tag `v1.0-good` and `master`). The current `master` branch compiles, but the algorithm fails to converge properly, resulting in statistically anomalous outputs (high energy states or oscillations) compared to the oracle.

To make matters worse, if you attempt to use `git bisect` to find the regression, you will discover that a large chunk of intermediate commits cannot be compiled due to a linker error that was introduced and later fixed. 

Your objectives are:
1. Analyze `/app/oracle_bin` to understand the expected behavior and convergence target. You can test it against the sample dataset at `/home/user/sample_data.csv`.
2. Find a way to bisect the repository to identify the exact commit that introduced the mathematical anomaly. You will need to interpret and bypass the linker errors during your bisection.
3. Diagnose the root cause of the convergence failure.
4. Fix the mathematical or statistical bug on the `master` branch.
5. Compile your fixed version and save the executable to `/home/user/optimized_engine_fixed`.

Your fixed binary must accept a CSV file as its first command-line argument and print its result to standard output in the exact same format as `/app/oracle_bin`. 

An automated verifier will test your `/home/user/optimized_engine_fixed` against `/app/oracle_bin` using a held-out dataset. The numerical output (e.g., the final energy or loss value) must match the oracle's output within a strict tolerance.