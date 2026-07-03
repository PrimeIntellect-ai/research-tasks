You are a researcher working on signal extraction from a dense sensor array. You have been given a dataset of raw sensor readings, but it is noisy. Your goal is to reshape this observational data, perform matrix decomposition to isolate the principal components, compute bootstrap confidence intervals to validate their stability, and calculate a distribution distance metric to quantify the information loss from noise reduction.

You must implement this workflow entirely in Rust. 

**Task Details:**

1. **Setup:**
   - Create a new Rust project at `/home/user/signal_analysis`.
   - You are provided with a CSV file at `/home/user/sensor_data.csv` with a header `time_idx,sensor_idx,reading`.

2. **Data Reshaping:**
   - Read the CSV and reshape the data into a 2D matrix of size $M \times N$, where $M$ is the number of unique `time_idx` values and $N$ is the number of unique `sensor_idx` values. Each cell $(i, j)$ should contain the `reading` for time $i$ and sensor $j$. (Assume the CSV is complete, but not necessarily sorted).

3. **Matrix Decomposition & Bootstrap (SVD):**
   - Compute the Singular Value Decomposition (SVD) of the $M \times N$ matrix.
   - Perform a bootstrap analysis to find the 95% confidence intervals for the **top 3 singular values**.
   - **Bootstrap procedure:** Perform 1000 iterations. In each iteration, sample $M$ rows from the original matrix *with replacement*, compute the SVD of this resampled matrix, and extract the top 3 singular values.
   - Calculate the 2.5th and 97.5th percentiles of the bootstrapped singular values to form the 95% confidence interval for each of the top 3 singular values.
   - *Requirement:* To ensure reproducibility, use the `rand_chacha` crate and initialize your random number generator with `ChaCha8Rng::seed_from_u64(42)` before starting the bootstrap loop. Use `nalgebra` for matrix operations.

4. **Information Loss (Distribution Distance):**
   - Reconstruct a denoised version of the original matrix using *only* the top 3 singular components (i.e., $U_3 \Sigma_3 V_3^T$).
   - Flatten both the original matrix and the reconstructed matrix.
   - Create a probability density histogram for both flattened datasets. Use exactly 50 equally spaced bins over the fixed range `[-10.0, 10.0]`. (Values exactly equal to 10.0 should go to the last bin; values outside this range can be ignored/dropped).
   - Normalize the histograms so they sum to 1.0 (representing probability distributions).
   - Compute the Euclidean ($L_2$) distance between these two discrete probability distributions.

5. **Output:**
   - Write a JSON file to `/home/user/analysis_output.json` with the following exact structure:
   ```json
   {
     "matrix_dimensions": [M, N],
     "top_3_svd": [
       { "value": <actual_sv_1>, "ci_lower": <boot_2.5th_1>, "ci_upper": <boot_97.5th_1> },
       { "value": <actual_sv_2>, "ci_lower": <boot_2.5th_2>, "ci_upper": <boot_97.5th_2> },
       { "value": <actual_sv_3>, "ci_lower": <boot_2.5th_3>, "ci_upper": <boot_97.5th_3> }
     ],
     "distribution_l2_distance": <computed_l2_distance>
   }
   ```

Compile and run your Rust program to generate the output file.