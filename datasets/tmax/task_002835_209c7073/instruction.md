You are a researcher working on numerical simulations where domain decomposition and parallel reduction order can lead to non-reproducible results due to floating-point truncation. 

Write a Python script at `/home/user/integration_study.py` that investigates this phenomenon by performing numerical integration, mesh refinement, and statistical analysis on the function $f(x) = \sin(x^2)$ over the interval $x \in [0, 5]$.

Your script must perform the following steps:

1. **Numerical Integration & Mesh Refinement**
   Implement a standard Trapezoidal rule to integrate $f(x)$ over $[0, 5]$. 
   Run a mesh refinement study calculating the integral for $N \in [1000, 2000, 4000, 8000, 16000]$ where $N$ is the number of intervals. 
   Calculate the absolute error for each $N$ compared to the high-precision reference analytical value: `0.5279172037233621`.

2. **Domain Decomposition & Floating-Point Reduction Simulation**
   For the finest mesh ($N=16000$), divide the integration domain into 160 contiguous, equal-sized blocks (each containing 100 intervals).
   Compute the local trapezoidal integral for each block exactly as it would contribute to the global integral. Cast each of the 160 block integrals to 32-bit floats (`numpy.float32`).
   
   To simulate non-deterministic reduction order in parallel environments:
   - Set `numpy.random.seed(42)`.
   - Generate 1000 different total sums. For each sum, randomly shuffle the 160 `float32` block integrals and then accumulate them sequentially using standard 32-bit floating point addition (e.g., standard python `sum()` on a list of `float32` or `numpy.sum` with `dtype=numpy.float32`). Record these 1000 total sums (converted back to standard floats).

3. **Bootstrap Confidence Intervals**
   Calculate the 95% Bootstrap Confidence Interval for the mean of those 1000 simulated sums using the percentile method.
   - Set `numpy.random.seed(42)` immediately before bootstrapping.
   - Use 10000 resamples (with replacement) of the 1000 sums.
   - Compute the mean for each resample.
   - Extract the 2.5th and 97.5th percentiles.

4. **Output Generation**
   Your script must save the results to `/home/user/results.json` with exactly the following JSON structure:
   ```json
   {
     "refinement_errors": [ /* array of 5 absolute errors */ ],
     "bootstrap_ci": [ /* [lower_bound, upper_bound] */ ],
     "true_value": 0.5279172037233621
   }
   ```

Run your script to produce the output file.