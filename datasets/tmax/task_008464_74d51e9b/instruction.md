You are a performance engineer analyzing a Monte Carlo simulation of random matrices to determine how often they become near-singular. Your objective is to write a rigorous C++ program that generates random matrices, computes their determinants, validates the empirical mean against a bootstrap confidence interval, and estimates the probability of near-singularity.

Write a C++ program at `/home/user/det_sim.cpp` that performs the following steps strictly in order, using `<random>` and a single `std::mt19937` generator seeded with `42`:

1. **Monte Carlo Generation:**
   - Initialize the generator: `std::mt19937 gen(42);`
   - Use `std::uniform_real_distribution<double> dist(0.0, 1.0);`
   - Generate $N = 100,000$ random $2 \times 2$ matrices where each entry $(X_1, X_2, X_3, X_4)$ is drawn from `dist` (in that exact order per matrix, i.e., $X_1$ first, then $X_2$, etc.).
   - Compute the determinant $D = X_1 X_4 - X_2 X_3$ for each matrix and store it in an array/vector `D`.
   - Calculate the sample mean of these determinants.
   - Count how many determinants satisfy $|D| < 0.01$ to calculate the empirical probability of a matrix being near-singular.

2. **Bootstrap Confidence Interval:**
   - Using the *same* generator instance (do not reseed it), create a `std::uniform_int_distribution<int> idx_dist(0, 99999);`
   - Perform $B = 1000$ bootstrap iterations. In each iteration, sample $N = 100,000$ elements from the original `D` array using `idx_dist(gen)` (draw exactly 100,000 indices per iteration) and calculate the mean of this bootstrap sample.
   - Sort the 1000 bootstrap means in ascending order.
   - Determine the 95% confidence interval using the percentile method: use the mean at index 25 (0-based) as the lower bound, and the mean at index 974 (0-based) as the upper bound.

3. **Output:**
   Compile and run your C++ program. Have it write the results to `/home/user/sim_results.txt` exactly in the following format, with values formatted to 6 decimal places:

```
Mean: <mean>
CI_Lower: <lower>
CI_Upper: <upper>
Prob_Near_Singular: <prob>
```

You may use standard Linux commands to compile (e.g., `g++ -O3 /home/user/det_sim.cpp -o /home/user/det_sim`) and execute the program.