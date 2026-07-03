You are a data analyst working on a performance-critical data pipeline. You need to process a dataset containing categorized vectors, apply a linear transformation (dot product) using a C program for speed, and aggregate the results to test the pipeline's reproducibility.

Your task is to:
1. Write a C program at `/home/user/process.c` that reads a CSV without headers from standard input. Each line has the format: `category,v1,v2,v3` (where `category` is a string up to 10 characters, and `v1, v2, v3` are floats).
2. For each row, the C program must calculate the dot product of the vector `[v1, v2, v3]` with the fixed weight vector `[0.5, 0.3, 0.2]`.
3. The C program should output the result to standard output in the format: `category,score` (where score is a float formatted to 2 decimal places).
4. Write a bash script `/home/user/run.sh` that:
   - Compiles `/home/user/process.c` into an executable named `process`.
   - Passes the input file `/home/user/data.csv` to the compiled program.
   - Pipes the output to a standard CLI tool (like `awk`) to aggregate (sum) the scores by category.
   - Sorts the aggregated output alphabetically by category.
   - Writes the final output to `/home/user/summary.csv` in the format `category,total_score` (where `total_score` is formatted to 2 decimal places).

The file `/home/user/data.csv` already exists. Ensure your `run.sh` script is executable (`chmod +x`) and runs without errors, consistently producing `/home/user/summary.csv`.