You are an ML Engineer tasked with preparing training data for a sensor reliability model. You have a dataset of sensor transmission successes and trials, but some of the legacy sensors failed to record the number of successful transmissions, leaving missing values in the data.

Unlike Python's Pandas, which might silently convert integer columns to floats when introducing `NaN` for missing data, you need to handle this strictly using Rust.

You must write a Rust program to perform Bayesian imputation for the missing values. 

Here are the requirements:
1. Initialize a new Rust project at `/home/user/bayes_prep`.
2. Configure your `Cargo.toml` with the necessary numerical and data parsing libraries (e.g., `csv`, `serde`).
3. Your program must read a CSV file located at `/home/user/sensor_data.csv`.
   The CSV has headers: `sensor_id,successes,trials`.
   Missing values in the `successes` column are represented as empty strings.
4. Implement Bayesian inference using a Beta-Binomial conjugate model:
   - Start with a global Beta prior for the success probability with `alpha = 2.0` and `beta = 5.0`.
   - Update this prior to a posterior distribution using *all* rows that have valid, non-missing `successes` data. (Remember: total successes are added to alpha, total failures are added to beta).
   - Calculate the posterior mean probability of success.
5. Impute the missing values:
   - For any row with a missing `successes` value, estimate the successes by multiplying the row's `trials` by the posterior mean probability.
   - Round this estimate to the nearest integer and use it as the imputed `successes` value.
6. Write the fully imputed dataset (including the originally valid rows) to `/home/user/cleaned_data.csv` in the same format and order as the input.
7. Write a log file to `/home/user/metrics.txt` containing the following exact three lines (replace the brackets with your calculated numbers formatted to 4 decimal places):
   Posterior Alpha: [value]
   Posterior Beta: [value]
   Posterior Mean: [value]

Ensure you compile and run your Rust program so that the output files are generated.