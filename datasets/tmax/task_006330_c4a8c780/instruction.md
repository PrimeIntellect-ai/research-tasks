You are a performance engineer tasked with analyzing the convergence scaling of a custom Monte Carlo simulation. You need to write the simulation in C, manage its build environment, and perform a linear regression on its error scaling.

Step 1: The Monte Carlo Simulation
Write a C program `/home/user/mc_pi.c` that estimates the value of Pi using a 2D Monte Carlo method.
- The program must take two command-line arguments: `seed` (an integer) and `N` (the number of points).
- Implement a Linear Congruential Generator (LCG) with the formula: `X_{n+1} = (1103515245 * X_n + 12345) % 2147483648`.
- Initialize the LCG with the given `seed`.
- For each of the `N` points, generate `x` then `y` (in that exact order). To map the LCG integer to a float in [0, 1), divide it by `2147483648.0`.
- Count how many points fall inside the unit circle (`x*x + y*y <= 1.0`).
- Print ONLY the estimated value of Pi to 6 decimal places.

Step 2: Scientific Environment Management
Create a `/home/user/Makefile` that compiles `mc_pi.c` into an executable named `mc_pi`.
- Use `gcc`.
- Include the following flags: `-O3 -Wall -Wextra`.
- Link the math library (`-lm`).

Step 3: Curve Fitting and Regression
We expect the absolute error $E$ of the Pi estimate to scale with $N$ roughly according to a power law: $E = c \cdot N^m$. Taking the natural logarithm yields: $\ln(E) = m \cdot \ln(N) + b$.
- Run your compiled `mc_pi` using a starting `seed` of `42` for the following values of `N`: `10000, 20000, 30000, 40000, 50000`.
- Note: Always restart the program with seed `42` for each run. Do not chain the generator across runs.
- Calculate the absolute error $E = |\text{Estimate} - \pi_{\text{true}}|$ for each run. Use `3.1415926535` as $\pi_{\text{true}}$.
- Perform an Ordinary Least Squares (OLS) linear regression of $\ln(E)$ against $\ln(N)$ across these 5 data points to find the slope `m` and intercept `b`. You may write a script (Python, Perl, etc.) to automate this.

Step 4: Reporting
Create a file `/home/user/scaling_report.txt` with exactly the following format:
Slope: <m>
Intercept: <b>

Round the slope and intercept to exactly 4 decimal places.