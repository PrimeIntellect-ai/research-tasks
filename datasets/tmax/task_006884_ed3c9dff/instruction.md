You are a machine learning engineer tasked with preparing physics-informed training data for a surrogate neural network. 

You have been provided with experimental measurements of a damped harmonic oscillator in `/home/user/noisy_data.csv`. The file contains two columns: `t` (time) and `y` (displacement). 

The underlying analytical model for the system is:
$$ y(t) = e^{-a t} \cos(b t) $$
where $a$ is the damping coefficient and $b$ is the angular frequency.

Your task is to estimate the true parameters and generate augmented training data by sampling from the posterior distribution. 

Perform the following steps:
1. Write a Python script `/home/user/prepare_data.py`.
2. In the script, load `/home/user/noisy_data.csv`.
3. **Optimization:** Use `scipy.optimize.minimize` (e.g., Nelder-Mead or L-BFGS-B) to find the best-fit parameters $(a, b)$ that minimize the Sum of Squared Errors (SSE) between the analytical model and the noisy data. Assume bounds $a \in [0.1, 2.0]$ and $b \in [1.0, 10.0]$.
4. **Validation:** Calculate the Sum of Squared Errors (SSE) between the data and the analytical model using your optimal best-fit parameters. Save this single float value to `/home/user/error.txt`.
5. **MCMC Sampling:** Using the `emcee` library, run a Markov Chain Monte Carlo sampler to estimate the posterior distribution of $(a, b)$. 
    - Assume a Gaussian log-likelihood: $\log P(y|t,a,b) = -0.5 \sum \left(\frac{y_i - y_{model}(t_i)}{\sigma}\right)^2$, with $\sigma = 0.1$.
    - Assume uniform priors over the bounds mentioned above.
    - Initialize 16 walkers near your optimized best-fit parameters.
    - Run the sampler for at least 1000 steps.
6. **Data Generation:** Extract the last 500 samples (from the flattened chain, discarding the burn-in period) and save them to `/home/user/posterior_samples.csv`. The CSV must have exactly two columns with the header `a,b`.

Ensure you run your script and verify that `/home/user/error.txt` and `/home/user/posterior_samples.csv` are created successfully.