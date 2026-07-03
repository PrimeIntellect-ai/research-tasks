You are a data analyst tasked with processing noisy thermal sensor data from manufacturing equipment. The data is located at `/home/user/sensor_data.csv` and contains three columns: `timestamp`, `machine_id`, and `temperature`.

The dataset suffers from missing values (sensor dropouts) and extreme outliers (sensor glitches). Your objective is to robustly estimate the true operating temperature of a specific machine using Bayesian inference, while ensuring strict pipeline reproducibility.

Please write and execute a Python script at `/home/user/analyze.py` that performs the following steps:

1. **Environment Setup**: Install necessary libraries (`pandas`, `pymc`, `arviz`) as needed.
2. **Data Processing**: 
   - Load `/home/user/sensor_data.csv`.
   - Filter the dataset to include only rows where `machine_id` is exactly `'M-101'`.
   - Handle missing values by dropping any rows where `temperature` is NaN.
3. **Bayesian Modeling**:
   - Instead of manually removing outliers, handle them robustly by modeling the `temperature` data using a Student-T likelihood.
   - Use the following priors for the Student-T distribution parameters:
     - Mean ($\mu$): Normal distribution with $\mu=50$, $\sigma=20$.
     - Scale ($\sigma$): HalfNormal distribution with $\sigma=10$.
     - Degrees of freedom ($\nu$): Exponential distribution with $\lambda=1/30$.
4. **Reproducibility & Sampling**:
   - Configure your numerical libraries and sampler to be strictly reproducible. 
   - Set the global random seed for NumPy to `42`.
   - Use PyMC to sample from the posterior. Configure the sampler with exactly: `draws=2000`, `tune=1000`, `chains=2`, `target_accept=0.9`, and set the PyMC sampler's random seed to `42`.
5. **Reporting**:
   - Calculate the posterior mean of $\mu$ and its 94% Highest Density Interval (HDI).
   - Export these results to `/home/user/results.json`. The JSON file must have exactly this format (keys must match exactly, values rounded to 3 decimal places):
     ```json
     {
       "mu_mean": 52.123,
       "hdi_3%": 50.456,
       "hdi_97%": 53.789
     }
     ```

To complete the task, your script `/home/user/analyze.py` must run successfully, produce the `/home/user/results.json` file, and running your script multiple times must yield the exact same numerical outputs in the JSON file.