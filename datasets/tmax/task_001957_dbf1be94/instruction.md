You are an AI assistant helping a computational mechanics researcher. The researcher needs you to run a Monte Carlo simulation to analyze the stochastic response of a mechanical system modeled by random stiffness matrices.

Please write and execute a Python script that performs the following steps:

1. **Environment Setup**: Ensure `numpy`, `scipy`, and `matplotlib` are installed.
2. **Monte Carlo Simulation**:
   - Set the `numpy` random seed to `42`.
   - Run `N = 500` Monte Carlo iterations.
   - In each iteration, generate a random symmetric positive-definite "stiffness" matrix $A$ of size $50 \times 50$.
   - To generate $A$: Create a $50 \times 50$ matrix $X$ where each element is drawn from a standard normal distribution $\mathcal{N}(0, 1)$. Compute $A = X X^T + 0.1 I$, where $I$ is the $50 \times 50$ identity matrix.
3. **Matrix Decomposition**:
   - For each matrix $A$, use Cholesky decomposition to solve the linear system $A y = b$, where the "load" vector $b$ is a vector of 50 ones.
4. **Numerical Integration**:
   - The solution vector $y$ represents discrete samples of a continuous response curve $y(t)$ at 50 evenly spaced points over the interval $t \in [0, 1]$.
   - Use Simpson's rule (from `scipy.integrate`) to numerically integrate $y(t)$ over the interval $[0, 1]$. Let this integral be $R$. Keep track of $R$ for all 500 iterations.
5. **Data Visualization & Logging**:
   - Create a histogram of the 500 $R$ values with 20 bins. Save the plot to `/home/user/response_histogram.png`.
   - Calculate the mean and standard deviation of the 500 $R$ values.
   - Output these statistics to a JSON file at `/home/user/simulation_results.json` with the following exact keys: `"mean_R"` and `"std_R"`.

Write the script, execute it, and ensure both the plot and the JSON file are created exactly as specified.