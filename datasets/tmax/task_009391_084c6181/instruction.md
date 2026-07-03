You are a Data Engineer building the transformation step of an ETL pipeline. We receive noisy temperature sensor data, and before loading it into our database, we need to apply a 1-Dimensional Kalman Filter (a form of recursive Bayesian inference) to smooth the data and estimate the true temperature. 

For performance reasons, this transformation step must be written in C.

I have placed a sample of raw sensor data at `/home/user/raw_sensor.csv`. The file has two columns: `Time` and `Measurement` (both are floats).

Your task is to write a C program, compile it, and run it to process this data.

**Requirements for the C program:**
1. Read the input data from `/home/user/raw_sensor.csv`.
2. Apply a 1D Kalman Filter to the `Measurement` column. Use the following parameters and formulas:
   - Initial State Estimate ($x_0$): `20.0`
   - Initial Estimate Uncertainty ($p_0$): `5.0`
   - Measurement Uncertainty / Noise ($r$): `2.0`
   - Process Noise ($q$): `0.1`

   **Filter Equations for each time step $t \ge 1$:**
   *Prediction Step:*
   - $x\_pred_t = x_{t-1}$
   - $p\_pred_t = p_{t-1} + q$

   *Update Step:*
   - Kalman Gain ($k_t$) = $p\_pred_t / (p\_pred_t + r)$
   - Current State Estimate ($x_t$) = $x\_pred_t + k_t \times (Measurement_t - x\_pred_t)$
   - Current Estimate Uncertainty ($p_t$) = $(1.0 - k_t) \times p\_pred_t$

3. Save the results to `/home/user/smoothed_sensor.csv`. The output file should have a header `Time,Measurement,Smoothed` and contain the original time, original measurement, and the updated state estimate ($x_t$) for each row, formatted to 4 decimal places (e.g., `%.4f,%.4f,%.4f`).
4. Calculate the Mean Squared Error (MSE) between the raw `Measurement` and the `Smoothed` estimate across all rows.
5. Save the MSE value to `/home/user/mse.txt`, formatted to exactly 4 decimal places (e.g., `%.4f\n`).

Please write your C code in `/home/user/filter.c`, compile it as `filter_exec`, and execute it to generate the required output files.