You are taking over a scientific computing project from a colleague. They were fitting a model using Markov Chain Monte Carlo (MCMC), but they left before finishing the sampler. 

You have been provided with an image file at `/app/formula.png` which contains the mathematical formula for the target unnormalized Probability Density Function (PDF) that needs to be sampled.

Your task:
1. Extract the mathematical formula for the target distribution from the image `/app/formula.png`. 
2. Create a Go project in `/home/user/mcmc/` and write a parallelized Metropolis-Hastings MCMC sampler from scratch to sample from this 2D distribution $(x, y)$. 
3. Run 4 independent MCMC chains in parallel using Go goroutines to ensure good mixing and convergence. 
4. Your colleague noted that calculating sample moments across chains previously yielded non-reproducible results due to floating-point addition order (race conditions in the summation loop). Ensure your reduction step (combining the chains to calculate the covariance matrix) is strictly deterministic and numerically stable.
5. Draw at least 500,000 samples per chain (discarding an appropriate burn-in period).
6. Calculate the variance of $x$, the variance of $y$, and the covariance of $x$ and $y$ from your aggregated samples.
7. Output these values as a JSON file at `/home/user/mcmc/cov.json` with the exact following keys: `"var_x"`, `"var_y"`, `"cov_xy"`.

Ensure your Go code is well-structured and uses standard libraries. You can use standard tools (like `tesseract`) to help read the image if necessary, or simply inspect it visually. Your final results will be evaluated on how closely your estimated covariance matches the true analytical covariance of the distribution.