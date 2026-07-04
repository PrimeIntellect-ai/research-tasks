You are a performance engineer profiling a suite of matrix decomposition algorithms (SVD, LU, QR, Cholesky) used in a scientific simulation pipeline. Recently, scientists noticed that running the pipeline in parallel environments produces slightly non-reproducible results compared to the serial reference dataset. You suspect this is due to floating-point reduction order variations in the multi-threaded math libraries.

Your task is to write a pure Bash script (using standard shell utilities like `awk`, `sort`, `paste`, etc.) that quantifies these floating-point deviations.

You have been provided with two directories containing output matrices from the algorithms:
1. Reference dataset (serial): `/home/user/data/ref_serial/`
2. Profiling dataset (parallel): `/home/user/data/run_parallel/`

Each directory contains four files:
- `svd_matrix.txt`
- `lu_matrix.txt`
- `qr_matrix.txt`
- `cholesky_matrix.txt`

The matrices are formatted as space-separated floating-point numbers. Corresponding files in both directories have the exact same dimensions.

Write a script at `/home/user/compare_matrices.sh` that does the following:
1. Iterates over the four algorithms (`svd`, `lu`, `qr`, `cholesky`).
2. Reads the corresponding matrix file from both directories.
3. Compares the matrices element-by-element to calculate the absolute difference between each corresponding element.
4. Finds the maximum absolute difference for each algorithm.
5. Writes the final results to `/home/user/report.txt`.

The output in `/home/user/report.txt` must follow exactly this format, sorted in descending order by the maximum difference:
Algorithm: <algo>, Max Diff: <max_diff>

For example:
Algorithm: qr, Max Diff: 0.045
Algorithm: svd, Max Diff: 0.015
...

Notes:
- The script must be executable (`chmod +x`).
- Do not use Python, R, or other higher-level scripting languages; you must rely on Bash built-ins, `awk`, and standard coreutils.
- Output differences should preserve the precision provided by default `awk` calculations.