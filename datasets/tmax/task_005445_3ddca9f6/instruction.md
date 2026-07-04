You are a machine learning engineer preparing a dataset of sensor readings for training. The data seems to contain some high-frequency artifacts that could cause issues when differentiated, similar to how near-singular inputs destabilize matrix factorization.

Your task is to analyze the data, test its numerical stability, and generate a report. 

You have been provided with two files:
- `/home/user/sensor_data.csv`: A 1D array of floats representing the raw sensor readings.
- `/home/user/ref_derivative.csv`: A 1D array of floats representing the expected reference derivative.

Write a Python script to perform the following steps:
1. Load both CSV files.
2. Compute the numerical derivative of the sensor data using `numpy.gradient` with default spacing (`dx=1.0`).
3. Compute the Mean Squared Error (MSE) between your calculated derivative and the reference derivative.
4. To test numerical stability, create a noisy version of the sensor data by adding a deterministic alternating noise. Specifically, add `1e-5 * (-1)**i` to the `i`-th element (where `i` is the 0-based index).
5. Compute the numerical derivative of the noisy data (again using `numpy.gradient` with default spacing).
6. Find the maximum absolute difference between the noisy derivative and the clean derivative.
7. Compute the numerical integral of the clean derivative using `numpy.trapz` (with default spacing `dx=1.0`).
8. Generate a single plot (e.g., using `matplotlib`) containing three curves: the original sensor data, its clean derivative, and the reference derivative. Save this plot to `/home/user/plot.png`.
9. Save your computed metrics to a text file at `/home/user/report.txt` in exactly the following format (round all values to 6 decimal places):

```
MSE: <value>
MaxDiff: <value>
Integral: <value>
```

Ensure your script runs successfully and creates both `/home/user/plot.png` and `/home/user/report.txt`.