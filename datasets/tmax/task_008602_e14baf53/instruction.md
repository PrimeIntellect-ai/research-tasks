You are a performance engineer tasked with profiling a hypothetical microservice's latency characteristics using statistical and numerical methods. 

Write a Bash script at `/home/user/profiler.sh` that performs the mathematical profiling described below. While the file must be a Bash script, you are encouraged to use inline Python (`python3 -c`) within the script to handle the complex mathematics, as `numpy` and `scipy` are available on the system.

When executed, `/home/user/profiler.sh` must perform the following pipeline and save the final computed values to a JSON file at `/home/user/results.json`.

Pipeline Requirements:
1. **Initialization**: Set the random seed to exactly `42` (if using Python, use `numpy.random.seed(42)`) to ensure reproducible results.
2. **Monte Carlo Simulation**: Simulate `10000` request latencies drawn from a Normal distribution with a mean ($\mu$) of `100.0` and a standard deviation ($\sigma$) of `15.0`.
3. **Density Estimation**: Fit a Gaussian Kernel Density Estimate (KDE) to these `10000` simulated latencies. Evaluate the probability density exactly at latency `110.0`.
4. **Matrix Decomposition**: 
   - Extract the first `100` simulated latencies from the array.
   - Reshape them into a `10 x 10` matrix $M$ (row-major).
   - Compute the symmetric positive-definite matrix $A = M^T M + I$ (where $I$ is the 10x10 identity matrix).
   - Compute the Cholesky decomposition of $A$, such that $A = L L^T$. 
   - Calculate the Frobenius norm of the lower triangular matrix $L$.
5. **Optimization**: Let $m$ be the empirical mean of the `10000` simulated latencies. Find the scalar $x$ that minimizes the cost function: $f(x) = (x - m)^2 + 0.5x$. (Use an initial guess of $x_0 = 100.0$).

Output Format:
Your Bash script must create exactly `/home/user/results.json` containing the three calculated metrics as floats rounded to exactly **4 decimal places**. The JSON must have the following exact keys:

```json
{
  "kde_110": <float>,
  "cholesky_norm": <float>,
  "optimal_x": <float>
}
```

Constraints:
- The script must be executable (`chmod +x /home/user/profiler.sh`).
- It must run to completion autonomously when executed.
- Do not hardcode the final mathematical answers in the script; the script must compute them.