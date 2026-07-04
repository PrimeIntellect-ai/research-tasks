You are a performance engineer working on a bioinformatics application. The application processes batches of DNA primer sequences, computes their k-mer frequency matrices, and attempts to perform a matrix decomposition to analyze sequence distance.

However, the current pipeline often crashes. Because some primers are highly conserved (highly similar), the resulting covariance matrix becomes near-singular or strictly singular, causing the Cholesky decomposition in the script to fail with a `LinAlgError`.

Your task is to fix the script, profile its performance over a dataset, and estimate the distribution of the execution times.

Here are your specific objectives:

1. **Fix the Matrix Decomposition:**
   The script `/home/user/analyze_primers.py` calculates a covariance matrix `C` and attempts to compute its Cholesky decomposition. 
   Modify the script so that instead of using Cholesky decomposition, it uses Singular Value Decomposition (SVD). 
   Specifically, compute the full SVD of `C`, reconstruct a low-rank approximation `C_k` using only the top 3 singular values (and their corresponding singular vectors), and replace the return value of the `process_matrix` function with the sum of all elements in the reconstructed matrix `C_k`.

2. **Run and Profile:**
   There are 100 data files in the directory `/home/user/data/` named `batch_1.txt` to `batch_100.txt`. 
   Write a bash script or command sequence to run `/home/user/analyze_primers.py` on each of these 100 files sequentially.
   For each run, measure the **real** execution time (in seconds). Save these 100 execution times to a file named `/home/user/times.txt`, with one execution time per line.

3. **Density Estimation:**
   Write a Python script `/home/user/fit_density.py` that reads the execution times from `/home/user/times.txt`.
   Use `scipy.stats.norm.fit` to fit a Normal distribution to these execution times.
   Write the resulting estimated mean and standard deviation to `/home/user/profile_results.txt` in the exact following format:
   `Mean: <mean>`
   `Std: <std>`
   (Replace `<mean>` and `<std>` with the floating-point values rounded to 4 decimal places).

Ensure all scripts are executable and the final output files are created at the specified paths.