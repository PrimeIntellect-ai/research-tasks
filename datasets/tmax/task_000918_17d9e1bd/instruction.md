You are a data scientist tasked with fitting a theoretical model to raw sensor data. 

An instrument has recorded a raw, unnormalized signal distribution across a spatial domain. The data is stored in an HDF5 file located at `/home/user/sensor_data.h5`. Inside this file, there are two datasets at the root level:
- `x`: The spatial coordinates (a 1D array of floats).
- `raw_signal`: The unnormalized signal amplitudes corresponding to `x`.

Your task is to analyze this data and compare it against a standard theoretical model by following these steps:

1. **Read the HDF5 data:** Extract the `x` and `raw_signal` arrays from `/home/user/sensor_data.h5`.
2. **Numerical Integration:** Calculate the definite integral of `raw_signal` with respect to `x`. You must use the composite trapezoidal rule (`numpy.trapz`) for all integrations in this task.
3. **Normalization:** Normalize the `raw_signal` by dividing it by the integral computed in step 2. This creates a valid probability density function, let's call it $p(x)$.
4. **Theoretical Model:** Generate the theoretical probability density function, $q(x)$, which is defined as a Standard Normal distribution (mean = 0, standard deviation = 1) evaluated at the same `x` coordinates. Use the standard formula: $q(x) = \frac{1}{\sqrt{2\pi}} \exp(-0.5 x^2)$.
5. **Distance Metric:** Calculate the Total Variation Distance (TVD) between the empirical normalized distribution $p(x)$ and the theoretical distribution $q(x)$. The TVD is defined as:
   $$TVD = 0.5 \int |p(x) - q(x)| dx$$
   Again, use `numpy.trapz` to perform this integration over the `x` domain.

**Expected Output:**
Create a JSON file at `/home/user/results.json` containing the calculated unnormalized integral and the total variation distance. The keys must be exactly `"raw_integral"` and `"tvd_distance"`. Round both values to exactly 4 decimal places. 

Example format of `/home/user/results.json`:
```json
{
  "raw_integral": 12.3456,
  "tvd_distance": 0.1234
}
```