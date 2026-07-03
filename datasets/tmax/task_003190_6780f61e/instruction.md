You are a data analyst investigating the accuracy of a legacy sensor forecasting model. You have been provided with a dataset at `/home/user/model_outputs.csv`.

Your goal is to process the data, handle missing values and outliers, and validate the model's accuracy, relying on statistical checks. You may use any combination of bash, `awk`, Python, or other standard CLI tools to accomplish this.

Here is what you need to do:

1. **Missing Value Handling**: Read `/home/user/model_outputs.csv`. Drop any rows where either `raw_value` or `model_prediction` is missing. Missing values are represented as empty strings, the exact string `"NaN"`, or the exact string `"NULL"`. 
   
2. **Outlier Detection**: On the remaining complete rows, calculate the **population** mean and **population** standard deviation of the `raw_value` column. Identify and drop any rows where the `raw_value` is strictly greater than `mean + (2 * std_dev)` or strictly less than `mean - (2 * std_dev)`.

3. **Output Validation**: For the clean dataset (after missing values and outliers are removed), calculate the Absolute Error between `raw_value` and `model_prediction` (`|raw_value - model_prediction|`). Count how many rows have an Absolute Error *strictly greater* than `0.5`. This is your `Failed Validation` count.

4. **Reporting**: Calculate the new population mean of the `raw_value` for the clean dataset. Write a final summary report to `/home/user/analysis_report.txt` using exactly the following format (replace the bracketed placeholders with your calculated numbers, rounding the mean to exactly 2 decimal places):

```text
Initial Complete Rows: [count_of_rows_after_dropping_missing]
Outliers Removed: [count_of_outliers_dropped]
Clean Mean Raw: [clean_mean_rounded_to_2_decimals]
Failed Validation: [count_of_rows_with_error_gt_0.5]
```

Do not include any other text in the `analysis_report.txt` file.