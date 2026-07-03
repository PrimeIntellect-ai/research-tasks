You are helping a data scientist automate their dataset cleaning and baseline modeling pipeline. We have a raw dataset located at `/home/user/data/raw_data.csv` with columns `id`, `featureA`, `featureB`, and `target`. 

Your task is to write a Python script at `/home/user/clean_and_test.py` and run it to perform the following steps:
1. **Numerical Library Configuration**: Before performing any calculations, configure `numpy` to raise an error on any floating-point division by zero or invalid operations (`np.seterr(divide='raise', invalid='raise')`).
2. **Model Fitting**: Load the dataset. Use `sklearn.linear_model.LinearRegression` to fit a model predicting `target` using `featureA` and `featureB`. 
3. **Model Output Validation & Outlier Detection**: Calculate the absolute error (residual) for every data point. Identify the `id` of the top 3 data points with the largest absolute errors (these are our suspected anomalies).
4. **Experiment Tracking**: Calculate the Mean Absolute Error (MAE) across the entire dataset. 
5. Save the results to an experiment log file at `/home/user/experiment_log.json` with the following exact JSON schema:
```json
{
  "top_3_outlier_ids": [id1, id2, id3],
  "mean_absolute_error": 1.2345
}
```
*Note: The `top_3_outlier_ids` list must be sorted in ascending order. The `mean_absolute_error` must be a float rounded to exactly 4 decimal places.*

Ensure your script runs successfully and creates the required JSON file.