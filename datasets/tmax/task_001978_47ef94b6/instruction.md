You are helping a developer debug a recent mathematical regression in our C++ query engine. The system processes text files containing numerical integration queries and outputs the results. Over the last 200 commits, our accuracy has dropped due to an undetected parsing or boundary condition bug, but we aren't sure exactly when or how it was introduced.

We have provided a known-good, stripped binary oracle from an older release at `/app/oracle_engine`.

Your task:
1. Navigate to the git repository at `/home/user/math_engine_repo`.
2. The `HEAD` commit is known to have the regression, while `HEAD~200` is known to be perfectly accurate. 
3. Create a minimal bash script to test the output of the compiled C++ program against the oracle `/app/oracle_engine`. Both executables take an input file path as the first argument and an output file path as the second argument.
4. Use `git bisect` to find the exact commit that introduced the bug.
5. Diagnose the issue (it is likely an off-by-one error or a parsing edge-case issue in `src/parser.cpp` or `src/integrator.cpp`).
6. Fix the code on the `main` branch (at `HEAD`).
7. Compile your fixed version into `/home/user/math_engine_repo/build/engine`.
8. Generate the final output file by running `/home/user/math_engine_repo/build/engine /home/user/math_engine_repo/test_queries.csv /home/user/math_engine_repo/final_output.csv`.

Ensure your final compiled executable is located precisely at `/home/user/math_engine_repo/build/engine` and the output is strictly placed at `/home/user/math_engine_repo/final_output.csv`.