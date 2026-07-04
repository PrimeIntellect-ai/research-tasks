You are a data analyst troubleshooting a machine learning pipeline script that fails to run. 

You have a dataset located at `/home/user/equipment_stats.csv` which contains sensor data for manufacturing equipment. The columns are `temp`, `pressure`, and `vibration`. 

There is an existing, broken Python script at `/home/user/train_model.py` that is supposed to process this data and train a model. Currently, it crashes because it does not handle missing data or sensor errors properly.

Your task is to fix or rewrite `/home/user/train_model.py` so that it performs the following steps in this exact order:
1. Load `/home/user/equipment_stats.csv` using pandas.
2. Impute any missing (NaN) values in the `pressure` column using the median of the existing `pressure` values.
3. Remove any rows where `temp` is greater than 100 (these are extreme outliers caused by sensor malfunctions).
4. Calculate the Pearson correlation coefficient between the cleaned `temp` and `pressure` columns.
5. Train a `sklearn.linear_model.LinearRegression` model using `temp` and `pressure` as the features (in that order) to predict `vibration`.
6. Write exactly two lines to a new file at `/home/user/metrics.log`:
   - Line 1: The Pearson correlation coefficient, rounded to exactly 4 decimal places (e.g., `0.1234`).
   - Line 2: The model coefficients for `temp` and `pressure`, comma-separated, rounded to exactly 4 decimal places (e.g., `0.5678,0.9101`).

Execute your script to ensure `/home/user/metrics.log` is created with the correct values.