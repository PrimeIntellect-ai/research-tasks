You are a machine learning engineer preparing synthetic training data to test the robustness of a new matrix factorization model. The model is known to fail on near-singular inputs or when parameter variance is too high, so you need to understand how the parameter estimates converge as the dataset size increases. 

Your task is to implement a Monte Carlo data generator, perform ordinary least squares (OLS) linear regression, and run a convergence test—entirely using standard Bash and CLI utilities (like `awk`).

**Step 1: The Monte Carlo Regression Script**
Create a Bash script at `/home/user/mc_regression.sh` that takes exactly two arguments: `N` (the number of data points) and `SEED` (the random seed).

The script must use `awk` to perform the following:
1. Initialize the random number generator using the provided `SEED` (e.g., `srand(seed)`).
2. Generate `N` random $(x, y)$ points where:
   - $x$ is uniformly distributed between 0 and 1.
   - The $noise$ is uniformly distributed between -0.5 and 0.5.
   - $y = 3.5x + 2.0 + noise$.
   *(Note: Generate $x$ first, then $noise$ for each point to maintain consistent RNG state progression)*
3. Calculate the line of best fit ($y = mx + c$) for these `N` points using the Ordinary Least Squares (OLS) closed-form formulas for slope ($m$) and intercept ($c$).
4. Print the result to standard output in the exact format: `N, m, c` (with $m$ and $c$ formatted to exactly 5 decimal places).

**Step 2: The Convergence Test**
Create a second Bash script at `/home/user/run_convergence.sh` that takes no arguments.
This script must:
1. Execute `mc_regression.sh` using a fixed `SEED` of `42`.
2. Run the regression for the following values of `N`: `10`, `100`, `1000`, `10000`, `100000`.
3. Save the combined output to a CSV file at `/home/user/convergence_log.csv`.

Ensure both scripts are executable. Do not use Python or other non-Bash/POSIX scripting languages. Rely strictly on standard shell tools (`bash`, `awk`, etc.).