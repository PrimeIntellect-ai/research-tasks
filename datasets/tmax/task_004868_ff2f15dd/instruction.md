You are an AI assistant helping a climate researcher organize and analyze recent sensor datasets.

The researcher has placed two CSV files containing raw sensor readings in the directory `/home/user/data/`:
1. `/home/user/data/batch_1.csv`
2. `/home/user/data/batch_2.csv`

Both files have the following columns: `sensor_id`, `temperature`, `humidity`, and `pressure`.

Your task is to write and execute a script (in Python, R, or any language of your choice) to process these datasets by performing the following steps:

1. **Tabular Data Transformation and Aggregation:**
   - Combine the data from both CSV files into a single dataset.
   - Calculate the average `temperature` for each `sensor_id`.
   - Save these aggregated results to `/home/user/agg_results.csv`. The file must contain exactly two columns with headers `sensor_id,avg_temperature`. The `avg_temperature` values must be rounded to exactly 2 decimal places. The rows must be sorted in ascending order by `sensor_id`.

2. **Regression Modeling:**
   - Using the combined dataset, fit a standard Ordinary Least Squares (OLS) Linear Regression model to predict `pressure` using `temperature` and `humidity` as the independent variables (features). Include an intercept in the model.

3. **Numerical Accuracy Testing:**
   - Calculate the Root Mean Squared Error (RMSE) of your regression model's predictions on the same training dataset.
   - Save the RMSE value to a file named `/home/user/model_metrics.txt`. The file should contain only the RMSE value, rounded to exactly 4 decimal places.

Make sure you create the exact files specified with the precise formatting requested.