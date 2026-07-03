You are a Data Scientist tasked with fixing an automated data cleaning and testing pipeline.

There is a Python script located at `/home/user/analyze.py` and a dataset at `/home/user/sensor_data.csv`. The script is currently failing to run properly. It is intended to process sensor readings, but it suffers from a missing backend configuration for plotting (causing crashes or blank plots in a headless environment), fails to enforce data schemas, and does not implement the required statistical testing.

Your task is to rewrite or fix `/home/user/analyze.py` so that it performs the following steps in exactly this order:

1. **Schema Enforcement**: Load `/home/user/sensor_data.csv`. Ensure the columns `temperature`, `pressure`, and `vibration` are cast to float. Drop any rows that contain data that cannot be cast to float (e.g., strings like "ERROR").
2. **Missing Value Handling**: Replace any `NaN` values in `temperature` and `pressure` with the median of their respective columns (computed *after* dropping invalid rows).
3. **Outlier Removal via Linear Algebra**: 
   - Extract the `temperature` and `pressure` columns as a 2D matrix (N x 2).
   - Compute the median vector $M = [\text{median}(\text{temperature}), \text{median}(\text{pressure})]$.
   - Compute the Euclidean distance (using linear algebra / vector norms) of each row's `[temperature, pressure]` from the median vector $M$.
   - Drop any rows where this distance is strictly greater than `20.0`.
4. **Hypothesis Testing**: Using the cleaned dataset, perform a 1-sample t-test on the `vibration` column against a population mean of `5.0`. Calculate the t-statistic and the 95% confidence interval for the mean.
5. **Plotting**: Generate a histogram of the cleaned `vibration` data and save it to `/home/user/vibration_hist.png`. You must ensure Matplotlib is configured correctly to save plots in a headless environment (no display attached) without producing blank files or crashing.
6. **Reporting**: Write a JSON file to `/home/user/report.json` with the following structure:
```json
{
  "t_stat": float, // Rounded to 4 decimal places
  "ci_lower": float, // Rounded to 4 decimal places
  "ci_upper": float, // Rounded to 4 decimal places
  "cleaned_rows": int // The number of rows remaining after outlier removal
}
```

Constraints:
- You may install any standard Python data science libraries (e.g., pandas, numpy, scipy, matplotlib) if needed.
- Write everything as part of `/home/user/analyze.py` and execute it.