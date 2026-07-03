You are a bioinformatics analyst working on modeling protein concentration inside a bioreactor over time. You have a time-series dataset of noisy spectroscopy readings representing the concentration of a target protein, located at `/home/user/spectroscopy_data.csv`. The file has 100 lines, each containing `time,concentration` (time goes from 0 to 99 in steps of 1).

Your task is to write a C program that processes this data, compares it against a theoretical mathematical model, and performs a statistical bootstrap to estimate the confidence interval of the error. 

Specifically, your C program (`/home/user/analyze.c`) must perform the following steps:

1. **Array Manipulation & Signal Processing:**
   Read the data into multi-dimensional arrays or structs. Smooth the noisy concentration data using a 5-point moving average. For each index `i` from 2 to 97 (0-indexed), the smoothed value `S[i]` is the average of the noisy concentrations at indices `i-2, i-1, i, i+1, i+2`. For the boundary indices (0, 1, 98, 99), keep the smoothed value exactly equal to the original noisy concentration.

2. **ODE Numerical Solving:**
   The theoretical concentration `C` follows the logistic growth differential equation: 
   `dC/dt = k * C * (1 - C / M)`
   where `k = 0.1` and `M = 100.0`.
   Using Euler's method with a step size of `dt = 1.0`, compute the theoretical concentration `C[i]` for time `i = 0` to `99`. The initial condition at `t = 0` is `C[0] = 1.0`.

3. **Error Calculation:**
   Calculate the squared error at each time step `i` (from 0 to 99): `E[i] = (S[i] - C[i])^2`, where `S[i]` is the smoothed signal (or original at boundaries) and `C[i]` is the theoretical ODE value.
   Compute the Mean Squared Error (MSE) over all 100 time steps.

4. **Bootstrap Confidence Intervals:**
   To estimate the 95% confidence interval of the MSE, use a bootstrap method:
   - Seed the random number generator strictly with `srand(42);` (this is required for reproducibility).
   - Perform 1000 bootstrap iterations.
   - In each iteration `b` (from 0 to 999), draw 100 random samples with replacement from the `E` array. Specifically, use `int idx = rand() % 100;` for each draw.
   - Calculate the mean of these 100 sampled squared errors and store it as `bootstrap_means[b]`.
   - After 1000 iterations, sort the `bootstrap_means` array in ascending order.
   - The lower bound of the 95% CI is the value at index 24 (the 2.5th percentile), and the upper bound is the value at index 974 (the 97.5th percentile).

5. **Output:**
   Write the results to a file named `/home/user/analysis_results.txt` with exactly the following format (use `%.4f` for all floating point values):
   ```
   MSE: <value>
   CI_LOWER: <value>
   CI_UPPER: <value>
   ```

Compile your C program, run it, and ensure the output file is generated correctly.