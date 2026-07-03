You are a machine learning engineer preparing a synthetic spectroscopy dataset for training a neural network. You've been given a simulation script that generates baseline signal profiles, but the data pipeline is currently suffering from reproducibility and numerical stability issues.

Your workspace is located at `/home/user/spectroscopy_ml/`. Inside, you will find:
1. `generate_spectra.py`: A script that solves a nonlinear response equation over a heavily refined 1D mesh (domain decomposition). It computes the total integrated energy of the spectrum. However, to simulate an asynchronous map-reduce pipeline, the domain chunks are returned out of order. Because standard floating-point addition is not perfectly associative, the total energy slightly fluctuates depending on the randomized reduction order, violating strict reproducibility requirements for your ML training baseline.
2. `observations.csv`: A dataset containing 500 noisy real-world observations of a specific spectral peak's intensity.

Your task consists of three phases:

**Phase 1: Numerical Stability & Code Correction**
Edit `/home/user/spectroscopy_ml/generate_spectra.py`. Identify the domain decomposition integration step where the total energy is summed. 
Currently, the script uses the standard `sum()` function on an unpredictably ordered list of floats, causing precision loss and non-reproducibility.
Fix this by replacing the standard sum with Python's strictly accurate, mathematically stable summation method (`math.fsum()`) which tracks multiple intermediate partial sums to eliminate precision loss regardless of input order. 
Run the corrected script to obtain the exact, stable total energy.

**Phase 2: Bootstrap Confidence Intervals**
Write a new Python script `/home/user/spectroscopy_ml/bootstrap_ci.py`. 
Load the `intensity` column from `/home/user/spectroscopy_ml/observations.csv`.
Calculate the 95% bootstrap confidence interval for the **mean** of these intensities.
Requirements for the bootstrap:
- Use exactly 10,000 resamples (with replacement).
- Set `numpy.random.seed(42)` immediately before generating your resamples to ensure reproducibility.
- Calculate the mean of each resample.
- Use the 2.5th and 97.5th percentiles of the bootstrap distribution as the lower and upper bounds of your confidence interval (e.g., using `numpy.percentile`).

**Phase 3: Output Reporting**
Create a final output file at `/home/user/spectroscopy_ml/results.json` containing the exact keys and formats:
```json
{
  "stable_energy": 12345.678901234567, 
  "bootstrap_ci_lower": 12.345,
  "bootstrap_ci_upper": 12.789
}
```
*Note: `stable_energy` should be the exact float printed by your corrected simulation. The CI bounds should be rounded to exactly 3 decimal places.*