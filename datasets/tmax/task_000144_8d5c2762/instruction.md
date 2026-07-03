You are a data scientist analyzing a noisy spectroscopic signal. The signal contains a Gaussian peak, but the baseline noise is highly correlated. You need to fit a model to the spectrum using a pre-generated set of Markov Chain Monte Carlo (MCMC) proposals to find the posterior mean.

Because the noise is correlated, you have been provided with a dense covariance matrix. Evaluating the likelihood requires matrix decomposition. You must write a C++ program to evaluate the proposals and trace the Markov chain.

**Model Specification:**
The spectrum model is a single Gaussian peak:
`f(x) = A * exp( - (x - mu)^2 / (2 * sigma^2) )`

The log-likelihood (ignoring constant terms) for a parameter set `(A, mu, sigma)` is:
`LL = -0.5 * (y - f)^T * Sigma^{-1} * (y - f)`
Where `y` is the observed spectrum vector, `f` is the model prediction vector, and `Sigma` is the covariance matrix.

**Your Task:**
1. Install the `Eigen3` C++ library (e.g., `libeigen3-dev`) to handle linear algebra.
2. Write a C++ program at `/home/user/mcmc_fit.cpp` that does the following:
   - Reads the 100-point observed spectrum from `/home/user/data/spectrum.csv` (two columns: `x`, `y`).
   - Reads the 100x100 covariance matrix from `/home/user/data/covariance.csv` (comma-separated, no headers).
   - Computes the Cholesky decomposition of the covariance matrix using Eigen (e.g., `Eigen::LLT`) to efficiently compute the quadratic form `(y - f)^T * Sigma^{-1} * (y - f)`.
   - Initializes the MCMC state with `A = 10.0`, `mu = 50.0`, `sigma = 5.0`.
   - Reads 1000 proposal states from `/home/user/data/proposals.csv` (columns: `A, mu, sigma`).
   - Reads 1000 uniform random numbers `u` from `/home/user/data/uniform.txt` (one float per line).
   - Iterates through the proposals `i = 0` to `999`:
     - Evaluates the log-likelihood `LL_prop` for the proposal.
     - Calculates the acceptance probability: `P = min(1.0, exp(LL_prop - LL_curr))` (assume a flat prior).
     - If `u[i] < P`, accept the proposal: update the current state and current log-likelihood.
3. Your C++ program must output the final accepted state (the last state after processing all 1000 proposals) to `/home/user/final_state.txt` in the format: `A,mu,sigma` (comma-separated, precise to at least 4 decimal places).

Compile and run your C++ code to generate the output file. You have sudo access to install necessary packages like `g++` and `libeigen3-dev` using `apt-get`.