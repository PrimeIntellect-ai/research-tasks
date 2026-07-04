You are a data engineer building an ETL pipeline that prepares datasets for downstream classification and regression models. As part of the data quality checks, you need to write a Python script that validates the incoming data schema, tests numerical stability using linear algebra, and runs a baseline regression model.

Create a Python script at `/home/user/etl_check.py` that performs the following tasks:

1. **Numerical Library Configuration:** At the very beginning of the script, configure `numpy` to raise exceptions (rather than warnings) for 'invalid' and 'divide' floating-point errors.
2. **Data Schema Enforcement:** Read the CSV file located at `/home/user/data/input.csv`. Ensure the data has exactly 4 columns (the first 3 are features `X`, the last is the target `y`). Drop any rows containing missing values (NaNs). Ensure all remaining data are cast to 64-bit floats.
3. **Numerical Accuracy & Linear Algebra:** Compute the condition number of the feature matrix `X` using `numpy.linalg.cond` (using the default 2-norm). This helps check for multicollinearity before downstream modeling. 
4. **Baseline Regression:** Perform a basic ordinary least squares linear regression $y = Xw$ using `numpy.linalg.lstsq` (with `rcond=None`). 
5. **Evaluation:** Calculate the Mean Squared Error (MSE) of the predictions from the baseline regression model on the same data.
6. **Reporting:** Save the results to `/home/user/output/report.json` in the exact following format:
```json
{
  "condition_number": 123.456,
  "mse": 0.123
}
```

Make sure the directories exist (create `/home/user/output` if needed). Run your script to generate the final JSON report.