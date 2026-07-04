You are a data engineer maintaining our mathematical ETL pipelines. We have two datasets that recently arrived in our system, but the previous engineer left before writing the final processing script. 

The two datasets are:
1. `/home/user/data/sensors.csv` - Contains time-series readings. Columns: `reading_id`, `sensor_id`, `temperature`, `pressure`
2. `/home/user/data/metadata.csv` - Contains target labels for regression and sensor properties. Columns: `sensor_id`, `humidity_baseline`, `target_metric`

Your task is to write a Python script at `/home/user/pipeline.py` that performs the following ETL and mathematical tasks:
1. Load both CSV files and perform an inner join on `sensor_id`.
2. Compute the Pearson correlation matrix for the joined dataset. Extract the exact correlation coefficient between `temperature` and `pressure`. Save this single float value, rounded to 4 decimal places, into `/home/user/output/corr.txt`.
3. Train a standard Linear Regression model (`sklearn.linear_model.LinearRegression`) to predict `target_metric` using `temperature`, `pressure`, and `humidity_baseline` as features.
4. To ensure pipeline reproducibility, you must perform a train-test split before training. Use `sklearn.model_selection.train_test_split` with `test_size=0.2` and `random_state=42`. Train the model on the training set.
5. Evaluate the model on the test set. Calculate the R^2 score (coefficient of determination). Save this single float value, rounded to 4 decimal places, into `/home/user/output/r2_score.txt`.

Ensure your script creates the `/home/user/output` directory if it does not exist, and writes the output files with just the numerical value (no extra text). You can run your script to generate the required files.