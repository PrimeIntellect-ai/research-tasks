You are a bioinformatics analyst tasked with building a reproducible computation pipeline to estimate the evolutionary distance between two DNA sequences. You need to implement a C++ program that calculates the maximum likelihood estimate of the Jukes-Cantor distance using a nonlinear equation solver, and then uses Markov chain Monte Carlo (MCMC) to sample the posterior distribution of this distance. Finally, you will wrap this in a bash script.

Here are the specific requirements:

1. **Input Data**: 
There is a file at `/home/user/sequences.txt` containing exactly two lines of DNA sequences of the same length.

2. **C++ Program (`/home/user/analyze_mutations.cpp`)**:
Write a C++ program that does the following:
   - **Data Parsing**: Read `/home/user/sequences.txt` and compute the total length $N$ and the number of differing positions $k$. The observed proportion of differences is $p = k/N$.
   - **Nonlinear Equation Solving**: In the Jukes-Cantor model, the relationship between distance $d$ and expected differences $p$ is $p = 0.75(1 - e^{-4d/3})$. Use the **Newton-Raphson method** to find the root of the function $f(d) = 0.75(1 - e^{-4d/3}) - p = 0$. 
     - Use an initial guess $d_0 = 0.1$.
     - Tolerance for convergence: $|f(d)| < 10^{-6}$.
     - Maximum iterations: 100.
     - Print the final estimate to standard output in the format: `MLE_d: <value>` (up to 6 decimal places).
   - **MCMC Sampling**: Implement a Metropolis-Hastings MCMC to sample the posterior distribution of $d$.
     - **Likelihood**: $\log L(d) = k \log(p(d)) + (N-k) \log(1-p(d))$ where $p(d) = 0.75(1 - e^{-4d/3})$.
     - **Prior**: Exponential distribution with rate $\lambda = 10$. $\log P(d) = \log(10) - 10d$ for $d>0$, and $-\infty$ otherwise.
     - **Proposal**: Normal distribution centered at the current $d$ with standard deviation $0.05$. 
     - Initialize the MCMC chain at the MLE $d$ found via Newton-Raphson.
     - Run the chain for exactly **10,000 iterations**. 
     - Use a fixed random seed for reproducibility: `std::mt19937 gen(42);`
     - You should use `std::normal_distribution<double>` for the proposal and `std::uniform_real_distribution<double>` for the acceptance step.
     - Output the $d$ value of each iteration (including the initial state as iteration 0, up to iteration 9999, totaling 10000 samples) to `/home/user/mcmc_samples.csv`, one value per line.

3. **Bash Pipeline (`/home/user/pipeline.sh`)**:
Write a bash script that:
   - Compiles `analyze_mutations.cpp` to an executable named `analyze` using `g++ -O3`.
   - Runs `./analyze`.
   - Uses standard Unix tools (like `awk` or `tail`) to calculate the arithmetic mean of the **last 5000** samples from `mcmc_samples.csv` (which represents the converged stationary distribution).
   - Appends the calculated mean to `/home/user/results.txt` in the format: `Mean_Posterior: <value>` (value should be a standard decimal).

Ensure `/home/user/pipeline.sh` is executable and does not require root privileges. All files must be placed exactly at the paths specified.