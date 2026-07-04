I am a researcher running simulations to extract periodic signals from noisy observational data. Previously, I used a script that attempted to fit a model using a custom matrix factorization method, but it constantly crashes with a `LinAlgError` due to near-singular inputs caused by collinearity in the Taylor-expanded design matrix.

I need you to write a new, robust Python script at `/home/user/mcmc_fit.py` that bypasses matrix inversion entirely by using a Markov Chain Monte Carlo (MCMC) approach to estimate the posterior distribution of the signal's parameters.

Here are the requirements:

1. **Data**: The data is located at `/home/user/observational_data.csv` with columns `t` and `y`.
2. **Model**: The signal follows the equation $y(t) = A \sin(2 \pi f t) + \epsilon$, where $\epsilon \sim \mathcal{N}(0, \sigma^2)$. Assume $\sigma = 0.5$ is known and fixed.
3. **Initialization via FFT**: 
   - Read and reshape the CSV data.
   - Compute the Fast Fourier Transform (FFT) of the `y` values.
   - Find the dominant frequency (the frequency corresponding to the maximum FFT amplitude, ignoring the zero-frequency DC component). 
   - Use this dominant frequency as the initial guess for $f$ ($f_{init}$).
   - Set the initial guess for $A$ to $1.0$.
4. **MCMC Sampling**:
   - Implement a simple Random Walk Metropolis-Hastings sampler.
   - **Priors**: Uniform prior for $A \in [0, 10]$ and $f \in [0, 10]$. (If a proposal falls outside this range, reject it).
   - **Likelihood**: Log-likelihood is $\sum_{i} \log(\text{PDF}_{\mathcal{N}}(y_i \mid A \sin(2 \pi f t_i), \sigma^2))$.
   - **Proposal Distribution**: Gaussian with standard deviations $\sigma_{prop, A} = 0.05$ and $\sigma_{prop, f} = 0.05$. Propose new $A$ and $f$ simultaneously.
   - Set the random seed strictly to `numpy.random.seed(42)` immediately before starting the MCMC loop.
   - Run the MCMC for exactly `20000` iterations.
5. **Output**:
   - Discard the first `5000` iterations as burn-in.
   - Calculate the mean of the remaining `15000` posterior samples for $A$ and $f$.
   - Save the results to `/home/user/results.txt` in the format `A_mean,f_mean` rounded to exactly 2 decimal places (e.g., `2.15,3.42`).

Write the script, run it, and ensure the `/home/user/results.txt` file is generated correctly.