You are a data scientist working on an embedded systems project where Python cannot be used. You need to build a C-based data cleaning and model training pipeline. 

There is a dataset at `/home/user/dataset.csv` containing sensor data with three columns:
1. `sensor_count` (Integer)
2. `temperature_celsius` (Float)
3. `failure_rate` (Float - Target Variable)

Due to upstream bugs, the dataset sometimes contains missing values (represented as empty strings between commas, e.g., `12,,0.5`), or explicit "NaN" strings. In pandas, this often silently converts integers to floats and propagates NaNs, ruining downstream models. We want to strictly enforce our schema in C.

Your task is to:
1. Install any necessary numerical libraries. We require you to use the GNU Scientific Library (GSL) for the mathematical modeling.
2. Write a C program at `/home/user/train.c` that parses `dataset.csv`.
3. Enforce the data schema: strictly parse each row. If any column is missing, empty, or contains non-numeric strings (like "NaN" or "N/A"), completely discard that row. Do not impute values.
4. Using the cleaned data, perform a Multiple Linear Regression to predict `failure_rate` ($Y$) based on `sensor_count` ($X_1$) and `temperature_celsius` ($X_2$). The model should include an intercept term ($X_0 = 1.0$).
5. Compile and run your program.
6. Output the final trained model coefficients to `/home/user/model_output.txt`.

The output file `/home/user/model_output.txt` must contain exactly three lines, formatted to 4 decimal places:
Intercept: [value]
Coefficient sensor_count: [value]
Coefficient temperature_celsius: [value]

Ensure your C code handles the file I/O, filtering, and model training efficiently.