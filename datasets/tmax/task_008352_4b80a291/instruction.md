You are acting as a bioinformatics systems analyst. We have extracted raw k-mer frequency counts from several DNA sequencing samples, but the data extraction pipeline flattened everything into a single-line CSV file. We need to reshape this data, perform a Principal Component Analysis step via Singular Value Decomposition (SVD), and compare the resulting singular values against a reference dataset of a known healthy cohort.

Your task:
1. You will find the flattened observational data in `/home/user/raw_kmer_counts.csv`. It contains 12 comma-separated floating-point numbers. Reshape this data into a 4x3 matrix (4 rows representing 4 samples, 3 columns representing 3 distinct k-mer frequencies) in row-major order.
2. Create a Rust binary project in `/home/user/svd_analyzer`.
3. In this Rust project, write a program that:
   - Reads the reshaped 4x3 matrix.
   - Uses the `nalgebra` crate (version "0.32" or compatible) to perform a Singular Value Decomposition (SVD) on the matrix to extract the 3 singular values.
   - Reads the reference singular values from `/home/user/ref_svs.txt` (which contains one reference float per line, ordered from largest to smallest).
   - Computes the absolute difference between your computed singular values (also ordered largest to smallest) and the reference singular values.
4. Compile your Rust program from source using `cargo build --release` and execute it.
5. Your program must output the final differences into a log file located at `/home/user/sv_diff.txt`. The file must contain exactly 3 lines, each containing the absolute difference for the respective singular value, formatted to exactly 2 decimal places (e.g., `0.46`).

Ensure you have all necessary permissions to create and compile files in `/home/user`.