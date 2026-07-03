You are an atmospheric data scientist. You have been given a raw dataset of barometric pressure readings taken from various weather balloons at different altitudes. Your task is to clean this observational data, fit an exponential decay model to find the sea-level pressure ($P_0$) and the scale height ($H$), and prepare the data for visualization.

The raw data is located at `/home/user/raw_obs.csv` with the following columns:
`id,altitude_m,pressure_hpa,sensor_status`

The atmospheric pressure $P$ at altitude $h$ is modeled by the equation:
$P(h) = P_0 e^{-h/H}$

Where:
* $P(h)$ is the pressure in hPa at altitude $h$
* $P_0$ is the sea-level pressure
* $H$ is the scale height in meters

By taking the natural logarithm of both sides, this becomes a linear equation:
$\ln(P) = \ln(P_0) - \frac{1}{H}h$

You must write a Go program at `/home/user/fit_model.go` that performs the following steps:
1. **Data Reshaping**: Read `/home/user/raw_obs.csv`. Discard any rows where `sensor_status` is not exactly `"OK"` or where `altitude_m` < 0.
2. **Model Fitting**: Perform an Ordinary Least Squares (OLS) linear regression on the filtered data using $x = altitude\_m$ and $y = \ln(pressure\_hpa)$. 
   * Calculate $P_0$ and $H$ from the resulting slope and intercept.
3. **Output Parameters**: Write the calculated parameters to a JSON file at `/home/user/model_results.json` in the exact format:
   `{"P0": 1013.25, "H": 8400.50}` (round both values to exactly 2 decimal places).
4. **Visualization Prep**: Generate a clean, comma-separated file for plotting at `/home/user/clean_plot_data.csv` with the header `altitude_m,actual_pressure,predicted_pressure`. Include only the filtered rows, sorted by `altitude_m` in ascending order. The `predicted_pressure` should be calculated using your fitted $P_0$ and $H$ values. Format the pressure columns to 2 decimal places.

To complete the task:
1. Write and run your Go program.
2. Ensure `/home/user/model_results.json` and `/home/user/clean_plot_data.csv` are created with the correct deterministic values.