You are an AI assistant helping a data analyst process a set of raw sensor readings.

You have been provided a dataset at `/home/user/sensor_data.csv`. The dataset contains sensor readings and a target value, but it is somewhat noisy and contains malformed rows.

Write a Python script that performs the following pipeline:

1. **Data Schema Enforcement:** Load the CSV. The valid schema requires the columns `s1`, `s2`, `s3`, `s4`, `s5`, and `target` to be strictly numeric (float or int). Find and drop any rows that contain non-numeric values (like strings, 'ERR', etc.) or missing values (NaN) in these specific columns.
2. **Dimensionality Reduction:** Extract the valid feature columns (`s1` through `s5`). Standardize these features (subtract mean, divide by standard deviation) and then apply Principal Component Analysis (PCA) to reduce them to exactly 1 principal component (PC1).
3. **Model Training and Evaluation:** Train a standard Linear Regression model using PC1 as the single predictor for the `target` variable. Calculate the $R^2$ (coefficient of determination) score of this model on the dataset.
4. **Reporting:** Write the final $R^2$ score to a file named `/home/user/metrics.txt`. The file should contain only the score, rounded to exactly 4 decimal places (e.g., `0.8412`).

Run your script to produce the `/home/user/metrics.txt` file.