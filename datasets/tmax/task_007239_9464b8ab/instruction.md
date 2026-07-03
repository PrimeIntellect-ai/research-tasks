You are a data scientist working on fitting models using Markov Chain Monte Carlo (MCMC). 

You have been given a C++ program located at `/home/user/mcmc_sampler.cpp` that uses the Metropolis-Hastings algorithm to sample from a target normal distribution $\mathcal{N}(\mu=5.0, \sigma=2.0)$. 

However, the sampler is currently failing to converge. Much like a numerical integrator that diverges due to a wrong step-size adaptation, the MCMC sampler is suffering from an extreme proposal step size, and there is also a critical logical bug in the acceptance ratio calculation.

Your task:
1. Identify and fix the logical bug in the Metropolis-Hastings acceptance ratio inside `/home/user/mcmc_sampler.cpp`.
2. Change the proposal step size (`delta`) to a sensible value (e.g., between 2.0 and 4.0) so the acceptance rate is healthy (roughly 20% to 50%).
3. Compile the program using `g++` and run it. 
4. Calculate the absolute error between the MCMC empirical mean (output by the fixed program) and the analytical mean of the target distribution ($\mu=5.0$).
5. Write ONLY this absolute error (a single floating-point number) to `/home/user/mean_error.txt`.

Ensure the final error is less than 0.1, proving your MCMC sampler correctly targets the distribution.