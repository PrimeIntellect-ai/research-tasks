You are an AI assistant helping a bioinformatics analyst with a sequence modeling pipeline. 

We are estimating the continuous adaptation parameters of a biological sequence model using Markov Chain Monte Carlo (MCMC). Our C++ program, located at `/home/user/mcmc_sequence.cpp`, performs a Random Walk Metropolis-Hastings algorithm to find the posterior distribution of a 3-dimensional parameter. 

However, the sampler is currently diverging and failing to mix. This is due to a "wrong step-size" adaptation analog: the multivariate normal proposal step is implemented incorrectly. Instead of using the Cholesky decomposition of the proposal covariance matrix to scale the standard normal vectors, the code directly multiplies the random vector by the full covariance matrix. 

Your tasks:
1. Download the Eigen 3.4.0 C++ library. Extract it such that the headers are accessible at `/home/user/eigen-3.4.0` (e.g., download from `https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz`).
2. Fix the bug in `/home/user/mcmc_sequence.cpp`. Locate the `generate_proposal` function. Use Eigen's `LLT` matrix decomposition to compute the lower-triangular Cholesky factor ($L$) of the `covariance` matrix, and correctly generate the proposal $x_{new} = x + L z$ (where $z$ is the standard normal random vector).
3. Compile the code using `g++ -std=c++11 -I /home/user/eigen-3.4.0 -O3 /home/user/mcmc_sequence.cpp -o /home/user/mcmc_sequence`.
4. Run the compiled binary `/home/user/mcmc_sequence`. 
5. The program should output the estimated posterior mean to `/home/user/posterior_mean.csv`. The file must contain exactly three comma-separated values (the x, y, and z means).

Do not change the random seed or the number of iterations in the C++ file, only fix the mathematical bug in the proposal generation.