As a bioinformatics analyst, you have received experimental data from a fluorometric thermal denaturation assay used to determine the melting temperature ($T_m$) of a novel DNA sequence. 

The dataset is located at `/home/user/data/melting_curve.csv` and contains two columns: `Temperature` (in Celsius) and `Fluorescence` (arbitrary units).

Your task is to write and execute a Python script to perform the following:
1. **Curve Fitting:** Fit a standard 4-parameter logistic (sigmoid) curve to the data to find initial parameter estimates. The function model is:
   $F(T) = L + \frac{U - L}{1 + \exp(-k \cdot (T - T_m))}$
   where $T$ is temperature, $F(T)$ is fluorescence, $L$ is the lower baseline, $U$ is the upper baseline, $k$ is the steepness, and $T_m$ is the melting temperature.
2. **MCMC Sampling:** Using the initial estimates, run a Markov Chain Monte Carlo (MCMC) sampler (you may use `emcee` or write a simple Metropolis-Hastings sampler) to estimate the posterior distribution of $T_m$. Assume uniform priors for all parameters and assume Gaussian measurement noise.
3. **Posterior Estimation:** Calculate the mean and the 95% credible interval (2.5th and 97.5th percentiles) of the $T_m$ marginal posterior distribution.
4. **Data Visualization:** Generate a plot of the raw experimental data overlaid with the best-fit curve (using the mean posterior parameters) and save it as `/home/user/results/fit_plot.png`.

You must output your numerical results to a JSON file at `/home/user/results/tm_posterior.json` with the following exact keys:
```json
{
  "tm_mean": 65.123,
  "tm_2_5": 64.500,
  "tm_97_5": 65.800
}
```
*(Values above are just examples).*

**Environment constraints:**
- Ensure you create the `/home/user/results/` directory if it does not exist.
- Standard scientific Python libraries (`numpy`, `scipy`, `pandas`, `matplotlib`, `emcee`) are available in the system environment.