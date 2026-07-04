You are an AI assistant helping a researcher analyze simulated spectroscopy data. 

I have a dataset of a measured optical spectrum located at `/home/user/spectrum.csv`. It contains two columns: `wavelength` (in nm) and `flux` (arbitrary units). The data contains a constant background baseline, a single emission peak, and Gaussian noise.

I need you to write and execute a Go program (`/home/user/analyze.go`) that performs the following scientific computing pipeline:

1. **Data Parsing:** Read the `/home/user/spectrum.csv` file.
2. **Signal Processing (Noise Estimation):** Assume the first 20 data points (by row order) contain no emission signal—only baseline and noise. Calculate the standard deviation of the `flux` values for these first 20 points. Let's call this `noise_sigma`.
3. **Peak Detection:** Find the maximum `flux` value in the entire original spectrum (`original_max_flux`) and its corresponding `wavelength` (`original_max_wavelength`).
4. **Monte Carlo Simulation:** I need to estimate the uncertainty of the peak flux measurement. Generate 10,000 mock spectra. A mock spectrum is created by taking the *original* spectrum's flux values and adding new random Gaussian noise to every point. The Gaussian noise must have a mean of 0 and a standard deviation equal to `noise_sigma`. 
   *(Important: Initialize your Go random number generator using a fixed seed of `42` via `rand.New(rand.NewSource(42))` so the results are reproducible).*
   For each of the 10,000 mock spectra, find the maximum flux value. Calculate the mean (`mc_mean_peak`) and standard deviation (`mc_std_peak`) of these 10,000 peak values.
5. **Statistical Hypothesis Testing:** We want to test the null hypothesis that the true peak flux is $\le 12.0$. Calculate the Z-score for the Monte Carlo mean: $Z = (\text{mc\_mean\_peak} - 12.0) / \text{mc\_std\_peak}$. Then, calculate the one-sided p-value for this Z-score (the probability of observing a value at least as extreme, assuming a normal distribution). You can use `math.Erfc` for this: $p = 0.5 \times \text{Erfc}(Z / \sqrt{2})$.
6. **Output:** Save the results to `/home/user/results.json` strictly in this format:
```json
{
  "noise_sigma": 0.0,
  "original_max_flux": 0.0,
  "original_max_wavelength": 0.0,
  "mc_mean_peak": 0.0,
  "mc_std_peak": 0.0,
  "p_value": 0.0
}
```

Ensure your Go code compiles and runs successfully, and leaves the `results.json` file on disk. Do not use external third-party Go libraries; standard library `math`, `math/rand`, `encoding/csv`, etc., are sufficient.