You are acting as a performance engineer who has just refactored a slow, legacy scientific simulation. You need to ensure the new, optimized version still produces statistically equivalent results compared to the baseline before replacing it.

A previous pipeline step generated an HDF5 file containing the output arrays from 50 runs of both the old and new algorithms. The file is located at `/home/user/profiling_data.h5`.

Inside this HDF5 file, there are two groups:
- `/v1_slow`: Contains 50 datasets named `run_0` to `run_49`.
- `/v2_fast`: Contains 50 datasets named `run_0` to `run_49`.

Each dataset contains an array of 5,000 `float64` values representing the simulation's energy outputs over time.

Your task is to perform a statistical regression test to verify if the output characteristics have changed. Write a Python script at `/home/user/verify_results.py` that does the following:

1. Opens `/home/user/profiling_data.h5`.
2. Calculates the standard deviation of each of the 50 runs in `/v1_slow`. You should end up with an array or list of 50 standard deviations.
3. Calculates the standard deviation of each of the 50 runs in `/v2_fast`. You should end up with another list of 50 standard deviations.
4. Performs a two-sample Kolmogorov-Smirnov test on these two sets of 50 standard deviations to check if they are drawn from the same continuous distribution. Use `scipy.stats.ks_2samp`.
5. Outputs the results to a JSON file at `/home/user/report.json` with exactly the following schema:
```json
{
  "ks_statistic": <float, rounded to 4 decimal places>,
  "p_value": <float, rounded to 4 decimal places>,
  "is_equivalent": <boolean, True if p_value > 0.05, otherwise False>
}
```

You may need to install necessary Python libraries (like `h5py` and `scipy`) using `pip`. Execute your script to generate the `/home/user/report.json` file.