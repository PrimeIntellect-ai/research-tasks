You are a data scientist working on a system that processes sensor data. You were previously trying to plot this data, but the visualization scripts kept failing or producing blank plots because the dataset contains `NaN` values, missing fields, and error flags that indicate corrupted rows. 

Instead of fixing the plot right now, your task is to write a Rust program to clean the dataset, compute the covariance between two sensors, and perform a Bayesian update on the sensor's mean reading.

The dataset is located at `/home/user/sensor_data.csv`. It has the following columns: `timestamp`, `sensor_a`, `sensor_b`, `error_flag`.

Write and run a Rust project (you can create it in `/home/user/cleaner`) that does the following:
1. Reads `/home/user/sensor_data.csv`.
2. Filters out and ignores any row that meets ANY of these conditions:
   - `error_flag` is `1`.
   - `sensor_a` or `sensor_b` is `NaN`, empty, or cannot be parsed as a valid floating-point number.
3. Computes the sample covariance (using $n-1$ in the denominator) between the valid `sensor_a` and `sensor_b` readings.
4. Performs a Bayesian update for the mean of `sensor_a` using the valid readings. 
   - Assume the prior distribution for the mean of `sensor_a` is a Normal distribution with $\mu_0 = 50.0$ and variance $\sigma_0^2 = 10.0$.
   - Assume the likelihood of the `sensor_a` observations is a Normal distribution with a *known* variance of $\sigma^2 = 25.0$.
   - Compute the posterior mean ($\mu_n$) and posterior variance ($\sigma_n^2$) for `sensor_a` given the $n$ valid observations.
   
The formulas for the Bayesian update of a Normal mean with known variance are:
- Posterior variance: $\sigma_n^2 = \frac{1}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}}$
- Posterior mean: $\mu_n = \sigma_n^2 \left( \frac{\mu_0}{\sigma_0^2} + \frac{n \bar{x}}{\sigma^2} \right)$
(where $n$ is the number of valid observations and $\bar{x}$ is the sample mean of the valid `sensor_a` readings).

Finally, your Rust program must output a JSON file to `/home/user/results.json` with exactly the following keys (and their corresponding computed float values):
- `"covariance"`
- `"posterior_mean"`
- `"posterior_variance"`

Ensure your Rust script compiles and runs successfully, and the JSON file is created with the correct values.