You are a data analyst tasked with processing a dataset of raw sensor readings that contains missing values and anomalies due to transmission errors. You need to write a Python pipeline to clean the data, apply a mathematical integration, and store the results.

The raw data is located at `/home/user/sensor_data.csv` with the columns: `timestamp`, `sensor_id`, `value`.

Please write a Python script that performs the following steps:
1. **Environment Setup**: Ensure your environment has the necessary libraries (e.g., `pandas`, `numpy`, `scipy`). You can install them using `pip`.
2. **Missing Value and Outlier Handling**:
   - For each `sensor_id`, calculate the mean and standard deviation of the `value` column (ignoring NaNs).
   - Identify outliers as any `value` where the absolute difference from the sensor's mean is strictly greater than 3 times the sensor's standard deviation. Replace these outliers with `NaN`.
   - Sort the data by `timestamp` in ascending order.
   - For each `sensor_id`, impute the `NaN` values using linear interpolation based on the `timestamp` (if your library supports index-based interpolation, set `timestamp` as the index first). 
   - If there are still `NaN` values at the beginning or end of a sensor's time series (which linear interpolation might miss), apply a forward-fill followed by a backward-fill per sensor.
3. **Mathematical Aggregation**:
   - For each `sensor_id`, compute the definite integral (area under the curve) of the cleaned `value` over `timestamp`. Use the composite trapezoidal rule (e.g., `numpy.trapz` or `scipy.integrate.trapezoid`).
4. **Data Storage and Reporting**:
   - Save the integration results to `/home/user/integration_results.csv`. It should contain two columns: `sensor_id` and `total_area`, sorted alphabetically by `sensor_id`.
   - Identify the sensor with the highest `total_area`. Write exactly the `sensor_id` and the `total_area` (rounded to 2 decimal places) separated by a comma to `/home/user/max_sensor.txt` (e.g., `SensorX,123.45`).

Write and execute your script to complete these tasks. Do not delete the original data file.