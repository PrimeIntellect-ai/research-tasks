You are a data scientist working on fitting a theoretical population model to observed time-series data. 

In your workspace `/home/user`, you have a dataset `/home/user/observed.txt` containing two columns: `time` and `population`.

You also have a buggy Python script `/home/user/simulate.py` that integrates the model's ordinary differential equation (ODE): 
$dP/dt = -k \cdot P \cdot (1 + \sin(t))$ with $P(0) = 100$.
Currently, this script takes the parameter $k$ as a command-line argument and prints the time and population to standard output. However, the numerical integrator diverges or oscillates wildly due to a hardcoded, inappropriately large step size.

Your task consists of three parts:

1. **Fix the Integrator**: Modify `/home/user/simulate.py` to use a stable integration method or a sufficiently small step size so that the solution is accurate and stable for $k$ values up to at least 2.0. The script must output the same number of time points (from $t=0$ to $t=10$ inclusive, one point per second, i.e., $t=0, 1, 2, ..., 10$).

2. **Parallel Parameter Search (Curve Fitting)**: Write a Bash script `/home/user/fit.sh` that performs a grid search to find the best parameter $k$.
   - Search the values of $k$ from `0.1` to `1.5` in increments of `0.1`.
   - You must evaluate the simulations in **parallel** using standard Bash features (like background jobs `&` and `wait`, or `xargs -P`).
   - For each $k$, calculate the Sum of Squared Errors (SSE) between the simulated population and the observed population in `observed.txt`.
   - Write the $k$ value that yields the lowest SSE to a file named `/home/user/best_k.txt`.

3. **Distribution Distance**: Once you have the best $k$, generate its simulated time-series. Calculate the Kolmogorov-Smirnov (KS) statistic (the distance metric) between the observed population values and the best-fit simulated population values. Save this single floating-point number to `/home/user/ks_dist.txt` (rounded to 3 decimal places).

Ensure all scripts are executable and that your final outputs are precisely located at `/home/user/best_k.txt` and `/home/user/ks_dist.txt`.