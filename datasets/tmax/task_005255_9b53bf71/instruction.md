You are assisting a researcher in fixing a scientific computing pipeline that simulates and analyzes spectrometer signals using Monte Carlo methods. 

Currently, the pipeline consists of a Bash script that runs multiple simulation iterations in parallel and aggregates the results. However, because the parallel processes complete in a non-deterministic order, the floating-point reduction (summation) happens in random orders. Since floating-point arithmetic is not strictly associative, this leads to non-reproducible final results.

Your task has three parts:

1. **Fix the Aggregation Script:**
   Inspect `/home/user/mc_sim/aggregate.sh`. It runs a Monte Carlo signal generation script (`/home/user/mc_sim/generate.py`) in parallel using `xargs`. The python script outputs lines in the format `run_index, val1, val2, ..., val100`. The bash script currently just strips the index and sums the values column by column using `awk`.
   Modify `/home/user/mc_sim/aggregate.sh` so that the intermediate outputs from the parallel runs are **sorted numerically by the `run_index`** before the index is stripped and the columns are summed. This will guarantee bit-for-bit reproducibility. Run the script to generate `/home/user/mc_sim/averaged_signal.txt`.

2. **Spectral Matrix Decomposition:**
   Write a new Bash script at `/home/user/mc_sim/analyze.sh`. This script must:
   - Read the 100 floating-point values from `/home/user/mc_sim/averaged_signal.txt` (which contains a single line of 100 comma-separated values).
   - Reshape these 100 values into a 10x10 matrix (row-major order).
   - Compute the Singular Value Decomposition (SVD) of this matrix.
   - You may use inline Python (`python3 -c` or a heredoc) within your Bash script to perform the matrix operations and SVD (using `numpy`).
   - Extract the top 3 largest singular values.

3. **Output Formatting:**
   The `analyze.sh` script must output the top 3 singular values, each on a new line, rounded to exactly 4 decimal places, to the file `/home/user/mc_sim/svd_top3.txt`.

Ensure your scripts are executable. Run both scripts to produce the final `svd_top3.txt`.