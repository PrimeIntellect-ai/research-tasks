You are a performance engineer profiling a mathematical simulation pipeline located in `/home/user/profiling_sim`. The pipeline consists of a C extension for heavy matrix operations, a Python script that calculates square roots recursively, and an SQLite database that logs profiling metrics.

Currently, the pipeline is completely broken. Your goal is to debug and fix it so it generates the final performance report. 

You need to resolve the following issues:
1. **Linker Error**: The C extension fails to build. The `build.sh` script throws an "undefined symbol" error when trying to compile `libmatrix.so`. You need to fix `build.sh` so it successfully compiles the shared library.
2. **Infinite Recursion due to Precision Loss**: The Python script `simulate.py` crashes with a `RecursionError`. The recursive function `calculate_sqrt(n, guess)` uses the termination condition `if guess == next_guess:`. Due to floating-point precision loss, it oscillates between two values and never converges. Modify `simulate.py` so the recursion terminates when the absolute difference between `guess` and `next_guess` is strictly less than `1e-7`.
3. **Query Result Debugging**: Once the script runs, it writes performance timings to an SQLite database (`metrics.db`) and queries it to print the average execution time. However, the query currently retrieves the `SUM` of execution times instead of the average. Fix the SQL query in `simulate.py` so it correctly computes and returns the `AVG(duration)`.

Once you have fixed `build.sh` and `simulate.py`, run `./build.sh` and then `python3 simulate.py`. 

The `simulate.py` script will automatically output a string in the format:
`Average execution time: <number> ms`

Create a file at `/home/user/profiling_sim/final_report.txt` and write *exactly* the output string printed by the fixed `simulate.py` script into this file.