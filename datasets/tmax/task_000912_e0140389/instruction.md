You are a Machine Learning Engineer preparing a training dataset from raw, noisy sensor logs. The downstream model you are building is highly sensitive to numerical instability and multicollinearity, so you need to rigorously clean the data and analyze its statistical properties.

Your task is to write and execute a Python script (`/home/user/prep_data.py`) that processes a CSV file located at `/home/user/sensor_data.csv`. 

You may install and use standard data science libraries like `pandas` and `numpy`.

Your script must perform the following pipeline in exactly this order:

1. **Missing Value Handling**: Read the CSV. Fill missing values by first applying a forward-fill (propagating the last valid observation forward), and then a backward-fill for any remaining missing values at the beginning.
2. **Outlier Removal**: After filling missing values, calculate the Z-score for every value in every column. Use the sample standard deviation (Delta Degrees of Freedom, `ddof=1`) and the sample mean for each column. Identify any row that contains at least one value with an absolute Z-score strictly greater than `3.0`. Drop these rows from the dataset. Keep track of the original row indices (0-indexed, based on the original CSV data rows) of the dropped rows.
3. **Correlation Analysis**: Compute the Pearson correlation matrix on the cleaned dataset. Identify all pairs of distinct features that have an absolute correlation greater than or equal to `0.90`. Represent each pair as a list of two string column names, sorted alphabetically (e.g., `["sensor_A", "sensor_C"]`). 
4. **Covariance & Numerical Accuracy**: Extract the cleaned data as a strictly `float64` NumPy array. Compute the sample covariance matrix of the features (where variables are columns, `ddof=1`). Calculate the determinant of this covariance matrix using `numpy.linalg.det`.

Finally, your script must output a JSON file at `/home/user/summary.json` with exactly the following structure:

```json
{
  "dropped_rows": [
    <integer original indices of dropped rows, sorted ascending>
  ],
  "correlated_pairs": [
    ["<col1>", "<col2>"],
    ... <list of highly correlated pairs, sorted alphabetically by the first column name, then the second>
  ],
  "cov_determinant": <float determinant value, rounded to 4 decimal places>
}
```

Ensure your script runs successfully and creates the `/home/user/summary.json` file.