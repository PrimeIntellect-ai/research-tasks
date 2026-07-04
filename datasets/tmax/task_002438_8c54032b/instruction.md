You are a computational researcher modeling a steady-state diffusion-decay process. You need to develop a reproducible computation pipeline that performs numerical simulation, analytical validation, and statistical analysis of noisy sensor data.

Your task has three main phases:

**Phase 1: Numerical Solver & Mesh Refinement**
Write a Python script (using `numpy` and `scipy`) that solves the following 1D boundary value problem using the finite difference method:
$u''(x) - u(x) = 0$ for $x \in [0, 1]$
Boundary conditions: $u(0) = 1$, $u(1) = 0$

1. Discretize the domain into $N$ intervals of equal length $h = 1/N$, yielding $N+1$ grid points $x_0, x_1, \dots, x_N$.
2. Use a standard second-order central difference approximation for the second derivative.
3. Compare your numerical solution to the exact analytical solution: $u_{exact}(x) = \frac{\sinh(1-x)}{\sinh(1)}$.
4. Start with $N=10$. If the maximum absolute error across all $N+1$ grid points is strictly greater than $1.0 \times 10^{-4}$, double $N$ (i.e., $10 \to 20 \to 40 \dots$) and re-solve.
5. Stop at the first $N$ where the maximum absolute error is $\le 1.0 \times 10^{-4}$. Let's call this `converged_N`.

**Phase 2: Data Generation**
You have been provided with the source code for a data generator in C at `/home/user/generator.c`.
1. Compile it using `gcc -O3 /home/user/generator.c -o /home/user/generator -lm`.
2. Run it with your converged $N$ as the only argument: `/home/user/generator <converged_N>`.
3. This will create a file named `/home/user/noisy_data.csv`. It contains 100 rows. Each row represents a simulated noisy measurement trial and contains exactly `converged_N + 1` comma-separated values corresponding to the values at the grid points $x_0 \dots x_N$.

**Phase 3: Bootstrap Confidence Intervals**
Write a Python script to analyze the generated noisy data:
1. For each of the 100 trials (rows), calculate the Mean Squared Error (MSE) between the noisy measurements and the *exact analytical solution* at those grid points. You will have 100 MSE values.
2. Use the bootstrap method to estimate the 95% confidence interval of the *mean* of these 100 MSE values.
   - Perform exactly 10,000 bootstrap resamples.
   - For each resample, draw 100 values with replacement from your original 100 MSE values, and calculate the mean of the resample.
   - Set the random seed for numpy to `42` (`numpy.random.seed(42)`) immediately before running the bootstrap loop.
   - Calculate the 2.5th and 97.5th percentiles of your 10,000 bootstrapped means to form the 95% confidence interval (use `numpy.percentile`).

**Final Output:**
Create a JSON file at `/home/user/result.json` with the following structure:
```json
{
  "converged_N": 20,
  "ci_lower": 0.012345,
  "ci_upper": 0.015678
}
```
Replace the values with your actual computed results. Round the confidence interval values to 6 decimal places.

All scripts must be executed and the final `result.json` must be present.