As a machine learning engineer, I need to prepare and validate a training dataset of acoustic signals. Our new simulation engine occasionally produces non-reproducible high-frequency artifacts due to floating-point reduction order issues, and I need to quantify how much this affects our features compared to our reference dataset.

I have two directories containing time-series data:
- `/home/user/data/reference/`: Contains 100 CSV files (`ref_0.csv` to `ref_99.csv`).
- `/home/user/data/simulation/`: Contains 100 CSV files (`sim_0.csv` to `sim_99.csv`).

Each CSV file has two columns: `time` (in seconds) and `amplitude`. The sampling rate is exactly 1000 Hz, and each file contains exactly 1000 samples (1 second of data).

Your task is to write a Rust program in `/home/user/analyzer` that performs the following data processing and regression testing:

1. **Spectral Analysis**: For each CSV file, compute the discrete Fourier transform (FFT) of the `amplitude` column. Calculate the magnitude of each frequency bin to find the "peak frequency" (the frequency between 0 Hz and 500 Hz, inclusive, that has the highest magnitude). 

2. **Statistical Analysis**: For a given dataset (directory), collect the peak frequencies of all 100 files. Compute the mean peak frequency. Then, use the bootstrap method to compute the 95% confidence interval for the mean peak frequency.
   - Use 10,000 bootstrap resamples (sample with replacement, same size as the original dataset).
   - Use the percentile method for the confidence interval (2.5th and 97.5th percentiles of the sorted bootstrap means).
   - To ensure reproducibility for the bootstrap, initialize a `rand_chacha::ChaCha8Rng` with a seed of `42`. Use this single RNG instance for all resampling. Do the reference dataset first, then the simulation dataset, using the same RNG sequentially.

3. **Output Generation**: Produce a JSON report at `/home/user/report.json` with the following precise structure:
```json
{
  "reference": {
    "mean_peak_freq": 50.12,
    "ci_lower": 49.50,
    "ci_upper": 50.80
  },
  "simulation": {
    "mean_peak_freq": 75.40,
    "ci_lower": 70.10,
    "ci_upper": 80.20
  }
}
```
*(The values above are just examples).*

**Requirements:**
- Initialize a standard Rust project in `/home/user/analyzer`.
- You may use the `rustfft`, `csv`, `serde`, `serde_json`, `rand`, and `rand_chacha` crates.
- Build and run the project so that `/home/user/report.json` is successfully created. 
- Ensure that you handle floating point comparisons correctly when finding the peak frequency. 
- Round the final output values in the JSON to 2 decimal places, or just output them as standard floats (the verifier will parse them as floats and check within a tolerance of `0.5`).