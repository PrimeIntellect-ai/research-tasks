You are a data engineer tasked with building a robust ETL pipeline that processes noisy IoT sensor data, enforces a strict schema, aggregates the data, and applies a sequential Bayesian update (a simplified Kalman filter) to estimate the true state of a system. 

You need to write a complete, reproducible Python pipeline that does the following:

**1. Environment Setup**
Create a bash script `/home/user/run_pipeline.sh` that installs any necessary Python libraries (e.g., pandas, numpy, jsonschema) into a virtual environment at `/home/user/venv` and runs your main Python script `/home/user/pipeline.py`.

**2. Data Ingestion & Schema Enforcement**
Read the raw sensor data from `/home/user/data/raw_sensors.csv`. 
Enforce the following data rules. Any row failing these rules must be entirely dropped from the analysis:
*   `timestamp`: Must be a valid ISO 8601 datetime string.
*   `sensor_id`: Must be an integer between 1 and 10 (inclusive).
*   `temperature_raw`: Must be a float between -50.0 and 150.0.
*   `pressure_raw`: Must be a float between 0.0 and 200.0.

**3. Tabular Transformation**
Convert the `timestamp` column to a datetime object.
Aggregate the valid data into 1-hour tumbling windows (e.g., '2023-10-01 00:00:00' to '2023-10-01 00:59:59').
For each 1-hour window, calculate the mean of `temperature_raw` and the mean of `pressure_raw`. Sort the aggregated windows chronologically.

**4. Sequential Bayesian Estimation (Linear Algebra)**
The system's true state is represented by a 2D vector $x = [T, P]^T$ (Temperature and Pressure).
Initialize the prior state estimate $x_0$ and covariance $P_0$ as:
$$x_0 = \begin{bmatrix} 20.0 \\ 100.0 \end{bmatrix}, \quad P_0 = \begin{bmatrix} 10.0 & 0.0 \\ 0.0 & 10.0 \end{bmatrix}$$

The measurement noise covariance matrix is known to be:
$$R = \begin{bmatrix} 2.0 & 0.5 \\ 0.5 & 3.0 \end{bmatrix}$$

For each 1-hour window $t$ (in chronological order), take the aggregated mean measurements as your observation vector $z_t$. Perform the following Bayesian update using matrix operations to find the posterior state $x_t$ and covariance $P_t$:
1.  Calculate Kalman Gain: $K_t = P_{t-1} (P_{t-1} + R)^{-1}$
2.  Update State Estimate: $x_t = x_{t-1} + K_t (z_t - x_{t-1})$
3.  Update Covariance: $P_t = (I - K_t) P_{t-1}$

*Note: $I$ is the 2x2 identity matrix. The superscript $-1$ denotes matrix inversion.*

**5. Output**
Save the final estimated states to `/home/user/output/estimates.csv`. 
The directory `/home/user/output/` might not exist, so your script should create it.
The output CSV must have exactly these columns:
`window_start`, `est_temperature`, `est_pressure`
*   `window_start`: The start of the 1-hour window formatted as `YYYY-MM-DD HH:MM:SS`.
*   `est_temperature`: The updated state $T$ rounded to 4 decimal places.
*   `est_pressure`: The updated state $P$ rounded to 4 decimal places.

Ensure `/home/user/run_pipeline.sh` is executable (`chmod +x`). 
Do not assume any packages are pre-installed except standard Python 3.10+ libraries. You may use `pandas` and `numpy` if your script installs them.