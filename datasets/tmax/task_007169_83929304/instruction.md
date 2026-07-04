You are acting as a data scientist modeling a reaction-diffusion process. We need to fit a parameter for our steady-state model and compare its predicted state distribution to empirical data.

You have an empirical probability distribution of particle counts in the file `/home/user/empirical.csv`.

Your task is to write, compile, and execute a C++ program that does the following:

1. **Solve a Non-Linear Equation:** Find the equilibrium parameter $\lambda$ (where $\lambda > 0$) by solving the equation:
   $$ \lambda e^\lambda = 15 $$
   You must implement a numerical root-finding algorithm (like Newton-Raphson or Bisection) in your C++ code to find $\lambda$ to an accuracy of at least $10^{-6}$.

2. **Generate a Predicted Distribution:** Using the calculated $\lambda$, compute a truncated Poisson distribution for the states $k = 0, 1, 2, 3, 4$. 
   The unnormalized probability for state $k$ is $Q'_{k} = \frac{e^{-\lambda} \lambda^k}{k!}$.
   Normalize these 5 values so they sum to exactly 1.0 to get your model distribution $Q$.

3. **Compute Probability Distribution Distance:** Read the empirical distribution $P$ from `/home/user/empirical.csv`. Compute the Kullback-Leibler (KL) divergence from $P$ to $Q$, defined as:
   $$ D_{KL}(P \parallel Q) = \sum_{k=0}^{4} P_k \ln\left(\frac{P_k}{Q_k}\right) $$
   *(Note: Use the natural logarithm).*

4. **Environment & Output:**
   - Create a clean directory `/home/user/fitter_project`.
   - Place your C++ source code there.
   - Write a `CMakeLists.txt` file to compile your code into an executable named `model_fitter`. Ensure it requires at least C++11.
   - Run the executable. Your program must write ONLY the final KL divergence value to a file at `/home/user/kl_result.txt`, formatted to exactly 6 decimal places (e.g., `0.123456`).

**Constraints:**
- Do not use external libraries for the root-finding or math other than the C++ standard library (`<cmath>`, etc.).