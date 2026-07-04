You are an AI assistant helping a researcher organize and analyze several datasets. The researcher is struggling because one of the files has missing IDs, causing an unexpected type conversion that breaks the data joining process.

You have three datasets located in `/home/user/data/`:
1. `/home/user/data/sensors.csv`: Contains `sensor_id`, `location`, and `installation_year`. Some `sensor_id` values are missing (empty).
2. `/home/user/data/readings.csv`: Contains `sensor_id`, `timestamp`, and `value`.
3. `/home/user/data/targets.csv`: Contains `sensor_id` and `target_metric`.

Your task is to write and execute a Python script to perform the following steps:
1. Load the three datasets using pandas.
2. Clean `sensors.csv` by dropping any rows where `sensor_id` is missing. Ensure the remaining `sensor_id` values are treated as integers to prevent float-conversion artifacts (like `1.0`) from breaking the joins.
3. Perform an inner join of all three datasets on `sensor_id`.
4. Run a bootstrap analysis on the `value` column of the joined dataset to estimate the 95% confidence interval of the mean. 
   - Set `numpy.random.seed(42)`.
   - Use exactly 1000 iterations. In each iteration, sample with replacement (sample size equals the number of rows in the joined dataset) and calculate the mean.
   - Calculate the 2.5th and 97.5th percentiles of these means using `numpy.percentile`.
   - Save the results as a comma-separated string `lower,upper` (each rounded to 4 decimal places) into a file named `/home/user/bootstrap_ci.txt`.
5. Train a `LinearRegression` model using `scikit-learn` on the joined dataset to predict `target_metric` using `value` and `installation_year` as features.
   - Calculate the Root Mean Squared Error (RMSE) of the predictions on the same training data.
   - Save the RMSE (rounded to 4 decimal places) into a file named `/home/user/rmse.txt`.

Ensure your python environment has the required packages (e.g., `pandas`, `numpy`, `scikit-learn`). You can install them via pip if necessary.