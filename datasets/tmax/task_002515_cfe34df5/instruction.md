You are a bioinformatics analyst tasked with modeling the multivariate distribution of interacting sequence motifs. 

You have a dataset of paired sequence features (Network Centrality and Motif Frequency) located at `/app/sequence_features.csv`. Previous literature has established a fixed covariance matrix for these specific features. We have provided a screenshot of this matrix from the supplementary materials of the original paper at `/app/target_cov.png`.

Your task is to build a robust C++ tool to estimate the posterior mean of these features using Markov Chain Monte Carlo (MCMC).

Here are your specific requirements:
1. **Extract Prior Knowledge:** Use OCR or any vision tools available to you to extract the $2 \times 2$ covariance matrix $\Sigma$ from `/app/target_cov.png`.
2. **Implement MCMC in C++:** Write a C++ program (e.g., `mcmc_sampler.cpp`) that implements a Metropolis-Hastings MCMC sampler to find the posterior distribution of the mean vector $\mu = [\mu_1, \mu_2]$.
    * **Likelihood:** Assume the data in `/app/sequence_features.csv` is drawn from a Bivariate Normal distribution $N(\mu, \Sigma)$, where $\Sigma$ is the fixed matrix you extracted.
    * **Prior:** Assume the prior for $\mu$ is a Bivariate Normal distribution with mean $[0.0, 0.0]$ and a diagonal covariance matrix $\begin{pmatrix} 10.0 & 0 \\ 0 & 10.0 \end{pmatrix}$.
3. **Convergence Testing:** Your C++ sampler must run at least 4 independent MCMC chains. Implement the Gelman-Rubin diagnostic ($\hat{R}$) across the chains. Your program should iteratively sample and calculate $\hat{R}$, stopping the sampling phase only when $\hat{R} < 1.02$ for both $\mu_1$ and $\mu_2$. Discard an appropriate burn-in period.
4. **Output:** Once convergence is reached, calculate the final posterior mean of $\mu_1$ and $\mu_2$ by pooling the post-burn-in samples from all chains. Save these two values (space-separated, floating point) to `/home/user/posterior_mean.txt`.

Ensure your C++ code is efficient and mathematically rigorous. You may write compilation scripts or helper scripts in bash/Python to manage the OCR and pipeline, but the MCMC sampling and convergence testing must be implemented from scratch in C++.