You are an AI assistant helping a bioinformatics analyst debug and fix a C++ Markov Chain Monte Carlo (MCMC) pipeline used for sequence analysis.

The analyst has written a tool that estimates mutation parameters by evaluating a Multivariate Normal (MVN) likelihood over k-mer frequency data. However, for highly repetitive biological sequences, the covariance matrix becomes near-singular. The current code uses Eigen's Cholesky decomposition (`LLT`), which fails on these near-singular matrices, causing the MCMC sampler to reject valid proposals and fail to converge.

Your task is to fix the pipeline, run the sampling, and produce the final posterior estimations.

Here are your specific instructions:

1. **Environment Setup**:
   - The project is located at `/home/user/bio_mcmc`.
   - You need to install the Eigen3 library for C++ (e.g., via `apt-get install libeigen3-dev` or similar) as the build depends on it.

2. **Fix the Likelihood Computation**:
   - Inspect `/home/user/bio_mcmc/likelihood.cpp`.
   - The function `compute_log_likelihood(const Eigen::VectorXd& x, const Eigen::VectorXd& mu, const Eigen::MatrixXd& cov)` currently attempts an `LLT` decomposition.
   - Replace the `LLT` logic with a robust approach using Singular Value Decomposition (SVD). 
   - Use `Eigen::JacobiSVD` (with `Eigen::ComputeThinU | Eigen::ComputeThinV`).
   - Compute the pseudo-inverse and the log-pseudo-determinant by ignoring singular values less than `1e-6`.
   - The log-likelihood formula to implement is:
     `log_L = -0.5 * (rank * log(2*PI) + log_pseudo_det + (x - mu)^T * pseudo_inverse * (x - mu))`
     where `rank` is the number of singular values >= `1e-6`.

3. **Build and Run the Pipeline**:
   - The project includes a `Makefile`. Run `make` to build the executable `mcmc_sampler`.
   - Run the sampler on the provided dataset: `./mcmc_sampler /home/user/bio_mcmc/data.csv`
   - The program will run an MCMC chain for 5000 iterations and print the posterior mean of the 3 parameters to stdout.

4. **Output the Result**:
   - Save the exact printed output (the posterior mean of the 3 parameters, comma-separated) into a file named `/home/user/bio_mcmc/final_mean.txt`.

Ensure the code compiles without errors and that the final log file contains exactly the output values.