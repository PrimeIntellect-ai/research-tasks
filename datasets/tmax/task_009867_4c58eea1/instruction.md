You are a bioinformatics analyst studying the accumulation of mutations in a viral lineage over time.

You are provided with observational data in `/home/user/sequences.csv`. This file contains two columns: `Day` and `Sequence` (a DNA sequence of length 50). The reference sequence at Day 0 is 50 'A's ("A" repeated 50 times). 

Your task is to:
1. **Reshape the Observational Data**: Write a C++ program or a Python script to process `/home/user/sequences.csv` and calculate the average number of mutations (Hamming distance from the reference sequence) for each distinct `Day`. Note that there are multiple sequences per day.
2. **ODE Modeling**: The mutation dynamics follow a simple ODE: $dM/dt = \alpha - \beta M$, where $M(t)$ is the average number of mutations at time $t$. 
3. **MCMC Sampling**: Write a C++ program that implements a Metropolis-Hastings MCMC algorithm to estimate the parameters $\alpha$ and $\beta$ from the reshaped data. 
    - Use a Gaussian likelihood function: $L \propto \prod \exp(-\frac{(M_{obs}(t) - M_{ode}(t))^2}{2\sigma^2})$. Assume $\sigma = 1.0$.
    - Use uniform priors for $\alpha \in [0, 10]$ and $\beta \in [0, 1]$.
    - Run 100,000 iterations, discarding the first 10,000 as burn-in. Use a step size of 0.05 for both parameters.
    - **Crucial**: Calculate $M_{ode}(t)$ using the analytical solution of the ODE to validate your numerical approach. Assume $M(0) = 0$.
    - **Note on Reproducibility**: To avoid floating-point reduction order issues, accumulate the log-likelihood strictly in order of increasing `Day`.
4. **Output**: Save the posterior means of $\alpha$ and $\beta$ into `/home/user/posterior_means.json` in the following exact format:
```json
{
  "alpha": 1.23,
  "beta": 0.45
}
```
Round the values to exactly two decimal places.

You may install any necessary C++ libraries or compilers using standard package managers (e.g., `sudo apt-get install g++`).