You are a performance engineer profiling a numerical simulation. Due to floating-point reduction order differences in the multi-threaded simulation engine, the spectral properties of the output matrices vary slightly between runs, causing non-reproducible behavior. 

To analyze this variance, 50 snapshots of the 10x10 system matrix have been captured and saved as a JSON file at `/home/user/matrices.json`. The file contains a single JSON array of 50 elements, where each element is a 10x10 2D array of floats.

Your task is to analyze the spectral gap fluctuations using Rust:
1. Create a new Rust project at `/home/user/svd_profile`.
2. Write a Rust program that reads `/home/user/matrices.json`.
3. For each of the 50 matrices, compute the Singular Value Decomposition (SVD) and extract the **largest singular value**. You should use the `nalgebra` crate (version 0.32 or compatible) for the matrix operations.
4. Compute the population mean and population standard deviation (N, not N-1) of these 50 largest singular values.
5. Write the result to `/home/user/svd_results.txt` in the exact format `mean,std`, with both values rounded to exactly 4 decimal places (e.g., `12.3456,0.1234`).

You may use any standard Rust crates (like `serde`, `serde_json`, `nalgebra`) by defining them in your `Cargo.toml`. Run your Rust program to generate the required output file.