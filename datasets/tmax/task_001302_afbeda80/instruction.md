You are a data engineer tasked with completing an ETL pipeline, reconstructing a simple anomaly detection model, and fixing a broken reporting script.

You have been provided with the following files in `/home/user/`:
1. `sensor_data.csv`: Raw sensor readings from multiple devices.
2. `model_weights.json`: Contains the coefficients and bias for a pre-trained Logistic Regression model.
3. `plot_heatmap.py`: A script intended to plot a correlation heatmap of the sensor data, but it currently fails or produces blank output in our headless Linux environment.

Your tasks are as follows:

**Phase 1: ETL & Feature Engineering**
Write a Python script (e.g., `pipeline.py`) that reads `/home/user/sensor_data.csv`.
The raw data has columns: `device_id`, `timestamp`, `sensor_A`, `sensor_B`.
Sort the data by `device_id` and then by `timestamp` in ascending order.
For each `device_id`, compute a new feature: `rolling_cov`. This is the rolling sample covariance between `sensor_A` and `sensor_B` over a window of 3 time steps.
*(Note: For the first two time steps of each device where a 3-step window is not available, fill the `rolling_cov` with 0.0).*

**Phase 2: Model Reconstruction & Inference**
The anomaly detection model is a standard Logistic Regression model. The features it expects, in exact order, are:
`[sensor_A, sensor_B, rolling_cov]`
Using the parameters in `/home/user/model_weights.json`, compute the anomaly probability for each row in your processed dataset.
The probability is calculated using the standard sigmoid function: P = 1 / (1 + exp(-z)), where z = bias + w1*sensor_A + w2*sensor_B + w3*rolling_cov.

Save the final dataframe to `/home/user/processed_data.csv` with exactly these columns:
`device_id`, `timestamp`, `anomaly_prob`
Round the `anomaly_prob` to 4 decimal places.

**Phase 3: Fix the Plotting Script**
The script `/home/user/plot_heatmap.py` is supposed to read `sensor_data.csv`, compute the correlation matrix of `sensor_A` and `sensor_B`, and save it as `/home/user/heatmap.png`. However, because our agent environment has no display attached, it crashes or produces a blank plot due to a backend misconfiguration.
Fix the script so that it successfully generates a valid PNG file at `/home/user/heatmap.png` containing the plot. Run the script to generate the image.

Ensure all outputs (`processed_data.csv` and `heatmap.png`) are located precisely at `/home/user/`.