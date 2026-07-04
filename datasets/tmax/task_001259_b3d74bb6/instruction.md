You are a data scientist analyzing mock astronomical spectroscopy data. You have been provided with an interferogram (a time-domain signal) from a newly commissioned instrument, and you need to determine the precise location and width of a specific spectral absorption feature.

The raw data is stored in an HDF5 file at `/home/user/data/interferogram.h5`. The file contains two datasets:
- `time`: A 1D array of time values (in seconds).
- `signal`: A 1D array representing the raw time-domain interferogram.

Your task is to:
1. **Load and Transform**: Read the `time` and `signal` data from the HDF5 file. Compute the corresponding amplitude spectrum of the signal using a discrete Fourier transform for real input (e.g., `np.fft.rfft`). Also compute the corresponding frequency bins. 
2. **Isolate the Feature**: Filter the frequency domain data to only include frequencies $f$ in the range $1.0 \le f \le 4.0$ Hz.
3. **Model the Spectrum**: Within this frequency range, the amplitude spectrum $S(f)$ is known to follow the model of a constant baseline with a single Gaussian absorption dip:
   $$S(f) = B - A \exp\left(-\frac{(f - f_0)^2}{2\sigma^2}\right)$$
   where $B$ is the baseline, $A$ is the absorption depth, $f_0$ is the central frequency of the feature, and $\sigma$ is the width.
4. **MCMC Fitting with Parallelization**: Use Markov Chain Monte Carlo (MCMC) to fit this model to the truncated amplitude spectrum and estimate the posterior distribution of the parameters. 
   - You must run your MCMC sampling in **parallel** using at least 4 parallel chains or workers (you can use Python's `multiprocessing`, `concurrent.futures`, `mpi4py`, or parallel features of an MCMC library like `emcee`).
   - Assume uniform/uninformative priors that cover reasonable ranges (e.g., $B \in [0, 20]$, $A \in [0, 10]$, $f_0 \in [1, 4]$, $\sigma \in [0.01, 1.0]$).
   - Use an appropriate Gaussian log-likelihood for the residuals.
5. **Output**: Calculate the mean of the posterior samples for $f_0$ and $\sigma$ (after discarding an appropriate burn-in period). Save these two values in a JSON file at `/home/user/results/fit_params.json` with the exact keys `"f_0"` and `"sigma"`.

Ensure that `/home/user/results/` exists before saving your output. Your final JSON file should look exactly like this:
```json
{
  "f_0": 2.501,
  "sigma": 0.205
}
```