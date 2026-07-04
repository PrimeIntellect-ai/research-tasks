You are a data engineer responsible for building and testing an ETL pipeline for IoT sensor data. 

We have a raw dataset `/home/user/raw_sensor.csv` containing dirty sensor readings, and a reference dataset `/home/user/reference_sensor.csv` containing high-quality, verified readings. 

Your goal is to write a C++ program (`/home/user/etl_pipeline.cpp`) that performs ETL on the raw data, applies a smoothing operation, and performs a parameter sweep (hyperparameter tuning) to find the optimal smoothing window size that minimizes the Mean Squared Error (MSE) compared to the reference dataset.

Here are the requirements for the ETL pipeline and tuning:
1. **Data Format**: Both CSVs have no header. Column 1 is an integer timestamp, Column 2 is a float value.
2. **Missing Value Handling**: In the raw dataset, some values are missing (represented as `"NaN"`). You must replace any `"NaN"` with the *global mean* of all valid (non-NaN) values in the raw dataset.
3. **Outlier Handling**: After handling missing values, cap any extreme outliers. An outlier is defined as any value that is greater than `mean + 3*std_dev` or less than `mean - 3*std_dev` (using the newly computed mean and standard deviation of the imputed dataset). Cap them exactly at these boundary values.
4. **Smoothing (Hyperparameter)**: Apply a Simple Moving Average (SMA) filter to the cleaned data. For a window size `W`, the smoothed value at index `i` is the average of the values from `i - W + 1` to `i` inclusive. (If `i - W + 1 < 0`, just average from index `0` to `i`).
5. **Numerical Accuracy Testing**: Calculate the Mean Squared Error (MSE) between your smoothed raw data and the `reference_sensor.csv` data.
6. **Tuning**: Test the window sizes `W` in `{1, 3, 5, 7, 9, 11}`. 

Compile your program, run it, and find the optimal window size `W` that yields the lowest MSE. 

Once you have the result, write it to `/home/user/best_param.txt` in exactly this format:
`W=[best_W], MSE=[lowest_MSE_rounded_to_4_decimal_places]`
(For example: `W=3, MSE=2.4512`)

You are restricted to standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<vector>`, `<cmath>`). You may use standard bash tools to explore the data.