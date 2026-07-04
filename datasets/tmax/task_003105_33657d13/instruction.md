You are an operations engineer triaging an incident. A critical data processing pipeline has crashed, leaving the system in an incomplete state. Your task is to fix the pipeline, recover the data, and successfully process the records.

You have been provided with a C program, `/home/user/pipeline.c`, which reads a write-ahead log (WAL) of transactions, recovers the state, and runs an iterative algorithm to find the equilibrium point of the data. 

However, the pipeline currently fails to run due to three distinct issues:
1. **Environment Misconfiguration**: The program relies on an environment variable `DATA_DIR` to locate the data files. It is currently crashing because this is not set correctly in your environment. The data file `wal.log` is located in `/home/user/data/`.
2. **Database Recovery (Corrupted WAL)**: The `wal.log` file experienced a partial write during the crash, resulting in a corrupted entry. The C program currently aborts when it encounters malformed lines. You must modify `pipeline.c` to gracefully ignore corrupted lines (lines that do not have exactly two parsed fields: an integer ID and a float value) and continue recovering the rest of the file.
3. **Convergence Failure**: After loading the data, the program runs an iterative smoothing algorithm. However, there is a bug in the convergence loop's logic (specifically how the `diff` is calculated) that causes it to either loop infinitely or diverge. You must fix the math in the convergence loop inside `pipeline.c` so that it correctly measures the absolute difference between iterations and converges.

Your goal is to:
1. Fix the environment configuration.
2. Modify `/home/user/pipeline.c` to fix the WAL parsing and the convergence loop.
3. Compile and run the fixed program.
4. The program is designed to write its final output to `/home/user/output.txt`. Ensure this file is generated successfully after the fixes.

Ensure your compiled program is named `pipeline` and is located in `/home/user/`.