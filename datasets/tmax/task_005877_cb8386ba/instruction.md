You are a data scientist tasked with analyzing custom sensor data. A colleague has provided a C program that generates this data, but you need to compile it, manage your Python environment, and compute robust statistics.

Perform the following steps:

1. **Compile Data Generator**: You will find a C source file at `/home/user/generate_data.c`. Compile this file from source using `gcc` into an executable named `/home/user/generate_data`.
2. **Generate Data**: Run the compiled executable to generate 1000 sensor readings. Redirect its standard output to a file named `/home/user/sensor_data.txt`.
3. **Scientific Environment Management**: Create a Python virtual environment at `/home/user/venv`. Activate it and install `numpy`.
4. **Bootstrap Confidence Interval**: Write a Python script at `/home/user/bootstrap_ci.py` using your virtual environment. The script must:
   - Read the values from `/home/user/sensor_data.txt`.
   - Set the numpy random seed exactly to `42` (`numpy.random.seed(42)`).
   - Perform a bootstrap analysis to find the 95% confidence interval of the **median** of the dataset.
   - Use exactly 10,000 bootstrap resamples. (Each resample should be drawn with replacement and be the same size as the original dataset).
   - Calculate the 2.5th and 97.5th percentiles of the bootstrapped medians using `numpy.percentile` (default settings).
5. **Output**: The script must save the results to `/home/user/ci_results.txt` in exactly this format (rounded to 4 decimal places):
   ```
   Lower: X.XXXX
   Upper: Y.YYYY
   ```

Run your script to produce the final `ci_results.txt` file.