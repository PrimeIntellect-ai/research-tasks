You are a data scientist tasked with cleaning a noisy dataset and performing statistical analysis. A raw dataset has been provided at `/home/user/raw_data.csv`.

Your task is to build a mini ETL pipeline and perform statistical tests on the cleaned data. Please follow these precise steps:

**Part 1: ETL Pipeline & Data Storage**
1. Read the dataset from `/home/user/raw_data.csv`. It contains the following columns: `timestamp`, `sensor_a`, `sensor_b`, `group`, and `value_c`.
2. Clean the data:
   - Drop any rows that have missing (NaN/null) values in either the `sensor_a` or `sensor_b` columns.
   - After dropping those rows, calculate the median of the `value_c` column.
   - Fill any missing values in the `value_c` column with this calculated median.
3. Save the cleaned dataset into an SQLite database located at `/home/user/cleaned_data.db`. Store the data in a table named `sensor_data`.

**Part 2: Statistical Analysis**
Using the cleaned data (you can read it from the SQLite database or continue your Python script):
1. Calculate the Pearson correlation coefficient between `sensor_a` and `sensor_b`.
2. Perform a two-sided Welch's t-test (independent two-sample t-test with unequal variances) to compare the means of `value_c` between the `treatment` group and the `control` group. 

**Part 3: Reporting**
Output your statistical results into a JSON file located at `/home/user/results.json`. The JSON file must have exactly the following keys, with values rounded to 4 decimal places:
- `"correlation"`: The Pearson correlation coefficient between sensor_a and sensor_b.
- `"t_statistic"`: The t-statistic from the Welch's t-test comparing `treatment` vs `control` (treatment array passed as the first argument, control array as the second).
- `"p_value"`: The p-value from the Welch's t-test.

Ensure your Python scripts handle the ETL and statistical calculations correctly. You may install any standard Python data science libraries (e.g., pandas, scipy, sqlite3) using pip if they are not present.