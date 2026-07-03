You are a data engineer tasked with building a robust ETL pipeline that not only transforms raw latency data but also validates numerical accuracy and performs statistical hypothesis testing. 

A raw dataset containing server response times has been placed at `/home/user/server_metrics.csv`. The dataset has two columns: `group` ('control' and 'treatment') and `latency` (float).

Please complete the following tasks:

1. **Analysis Environment Setup:**
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `pandas`, `scipy`, and `pytest` in this virtual environment.

2. **ETL and Statistical Modeling Script:**
   - Write a Python script at `/home/user/etl.py` that processes `/home/user/server_metrics.csv`.
   - **Tabular Aggregation:** Group the data by `group`. For the `latency` column, calculate the `count`, `mean`, and `std` (sample standard deviation, ddof=1).
   - **Confidence Intervals:** Calculate the 95% confidence interval for the mean of each group using the Student's t-distribution.
   - Save the aggregated data to `/home/user/transformed_metrics.csv`. Ensure the CSV has exactly the following columns: `group`, `count`, `mean`, `std`, `ci_lower`, `ci_upper`. Round all float values to 4 decimal places before saving.
   - **Hypothesis Testing:** Perform an independent two-sample t-test (Welch's t-test, assuming unequal variances) comparing the `latency` of the 'control' group vs the 'treatment' group.
   - Save the test results to `/home/user/ttest_results.json` with exactly two keys: `"t_stat"` and `"p_value"` (both floats, not rounded).

3. **Numerical Accuracy Testing:**
   - Write a test script at `/home/user/test_etl.py` using `pytest`.
   - Write a test function named `test_numerical_accuracy()` that calculates the 95% confidence interval for a hardcoded dummy array: `[10.0, 12.0, 14.0, 15.0, 11.0]`.
   - Assert that the calculated `ci_lower` is exactly `9.95` and `ci_upper` is exactly `14.85` (when rounded to two decimal places).
   - Run the test suite using your virtual environment's `pytest` and pipe the standard output to `/home/user/pytest_output.txt`.

Ensure all files are created exactly at the specified paths. Execute your ETL script to generate the final CSV and JSON files, and run the pytest suite to generate the test output log.