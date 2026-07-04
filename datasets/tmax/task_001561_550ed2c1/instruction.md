You are tasked with analyzing a noisy acoustic signal to extract and model its underlying frequency trajectory. 

We have recorded a 1-second audio file located at `/app/signal.wav` (sample rate: 8000 Hz). The signal contains a noisy chirp whose instantaneous frequency $f(t)$ (in Hz) follows an exponential curve:
$$f(t) = \alpha e^{\beta t} + \gamma$$

Your objective is to robustly estimate the parameters $\alpha$, $\beta$, and $\gamma$. Because the data is noisy, you must use a Bayesian approach to find the posterior mean of these parameters.

Please perform the following steps:
1. **Signal Processing:** Extract the instantaneous frequency over time from the audio file (e.g., using a short-time Fourier transform/spectrogram peak tracking).
2. **Optimization:** Use an optimization algorithm (like Nelder-Mead or L-BFGS) to fit the curve and find the Maximum A Posteriori (MAP) or Maximum Likelihood estimate for $\alpha$, $\beta$, and $\gamma$. Use this as your starting point.
3. **MCMC Sampling & Parallel Computing:** Implement an MCMC sampler (e.g., Metropolis-Hastings or via a library like `emcee` or `PyMC`) to draw samples from the posterior distribution of the parameters. To speed this up, you **must** parallelize the sampling process, running at least 2 independent Markov chains concurrently using a parallel computing framework (like `multiprocessing`, `joblib`, or `mpi4py`).
4. **Estimation:** Calculate the posterior mean for each parameter from your chains (after discarding an appropriate burn-in).

Save your final posterior mean estimates to a JSON file at `/home/user/estimates.json` in the exact following format:
```json
{
  "alpha": 123.45,
  "beta": 1.23,
  "gamma": 123.45
}
```

You may use any programming language of your choice. Ensure your code handles the necessary imports, package installations, and execution within the terminal.