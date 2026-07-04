You are an AI assistant helping a researcher organize and analyze a dataset of sensor measurements. The researcher needs a fast, compiled ETL (Extract, Transform, Load) pipeline and Bayesian inference tool written in C++.

You must create a C++ program at `/home/user/etl_bayes.cpp`, compile it to `/home/user/etl_bayes`, and run it.

The program should read a CSV file located at `/home/user/measurements.csv` containing raw sensor data. 

**1. Data Schema Enforcement (ETL)**
The CSV has no header. Each row has three comma-separated columns: `sensor_id`, `measurement`, and `status`.
You must filter the dataset row by row. A row is ONLY valid if:
- `sensor_id` is a strictly positive integer (> 0).
- `measurement` is a valid floating-point number.
- `status` is exactly the string `"OK"`.
Invalid rows should be ignored (dropped).

**2. Bayesian Inference & Probabilistic Modeling**
For the valid measurements, you will perform a simple Bayesian update to estimate the true mean of the measurements. 
Assume the following:
- The prior for the mean $\mu$ is a Normal distribution with $\mu_0 = 0.0$ and variance $\sigma_0^2 = 1.0$.
- The likelihood of each measurement is normally distributed with a known variance of $\sigma^2 = 1.0$.
- For $n$ valid measurements with a sum of $S$, the posterior variance is $\sigma_n^2 = \frac{1}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}}$.
- The posterior mean is $\mu_n = \sigma_n^2 \left( \frac{\mu_0}{\sigma_0^2} + \frac{S}{\sigma^2} \right)$.

Using the values $\mu_0=0.0$, $\sigma_0^2=1.0$, and $\sigma^2=1.0$, these formulas simplify nicely.

**3. Model Evaluation / Output Format**
After parsing the file and calculating the posterior mean and variance, your C++ program must output a JSON file to `/home/user/posterior.json` with exactly this format:
```json
{
  "posterior_mean": <float_value>,
  "posterior_variance": <float_value>
}
```
Round the floating-point values to 4 decimal places.

Write the C++ code, compile it using `g++`, and run it so that `/home/user/posterior.json` is generated correctly.