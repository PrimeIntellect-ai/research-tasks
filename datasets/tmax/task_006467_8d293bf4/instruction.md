You are a bioinformatics analyst tasked with processing raw electrical signal data from a nanopore sequencer. The sequence translocation event has produced a noisy pulse in the current.

The raw signal is located at: `/home/user/signal_data.csv`
It contains two columns: `time` (in milliseconds) and `current` (in picoamperes).

Your objective is to denoise this signal, extract the precise event peak using optimization, and estimate the uncertainty of the event duration using MCMC sampling. 

Perform the following steps and output the final metrics to a JSON file. You may write scripts in any language (e.g., Python, R) to accomplish this.

**Step 1: Signal Processing**
The signal is corrupted by high-frequency electronic noise (frequencies $\ge 1.0$ kHz, assuming `time` is in ms so frequency is in $ms^{-1}$ or kHz). Apply a Fourier-based low-pass filter to completely remove all frequency components $\ge 1.0$ kHz from the `current` data. 
Find the time at which this filtered signal reaches its absolute maximum. Let this be `T_peak`.

**Step 2: Optimization**
Isolate a window of the filtered signal around the peak: `T_peak - 5.0 <= time <= T_peak + 5.0`.
Fit a non-linear Gaussian pulse model to this window to find the exact peak parameters:
$I(t) = a \cdot \exp(-c \cdot (t - \mu)^2) + b$
Use an optimization algorithm (e.g., Levenberg-Marquardt or Gradient Descent) to estimate the parameters $a$, $c$, $\mu$, and $b$. 

**Step 3: MCMC Sampling for Posterior Estimation**
We need to estimate the uncertainty of the inverse-width parameter `c` (which corresponds to the translocation speed).
Implement a Metropolis-Hastings MCMC sampler to estimate the posterior distribution of `c`. 
- Fix $a$, $\mu$, and $b$ to the exact optimized values found in Step 2.
- Assume the observations in the filtered window follow a Normal likelihood around the model $I(t)$ with fixed standard deviation $\sigma = 0.2$.
- Use a Uniform prior for $c$ in the range $[0.01, 2.0]$.
- Use a Normal proposal distribution centered on the current `c` with standard deviation $0.05$.
- Set your random seed to `42` (e.g., `np.random.seed(42)`).
- Initialize the MCMC chain at your optimized value of $c$.
- Run $10,000$ iterations. Discard the first $2,000$ iterations as burn-in.
- Calculate the posterior mean of `c` from the remaining samples.

**Output Generation**
Create a JSON file at `/home/user/analysis_report.json` containing the following exact keys and your computed numerical values:
```json
{
  "T_peak": <float, from Step 1>,
  "optimized_mu": <float, from Step 2>,
  "optimized_a": <float, from Step 2>,
  "posterior_mean_c": <float, from Step 3>
}
```
Round all float values in the JSON to 3 decimal places.