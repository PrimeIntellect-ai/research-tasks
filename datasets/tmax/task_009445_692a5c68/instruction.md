You are a data analyst working for a manufacturing company. The engineering team has provided you with a dataset of sensor readings from the assembly line, located at `/home/user/sensor_data.csv`. They want you to analyze the correlations between the sensors and the production outcomes, and then build baseline predictive models.

The dataset contains four sensor features: `temperature`, `pressure`, `humidity`, and `vibration`. 
It also contains two target variables: `defect` (binary: 1 if defective, 0 if not) and `yield_strength` (continuous numeric).

Please perform the following tasks:

1. **Correlation Analysis**:
   - Calculate the Pearson correlation coefficient between all four sensor features and the two target variables.
   - Identify the single sensor feature that has the highest absolute correlation with `defect`.
   - Identify the single sensor feature that has the highest absolute correlation with `yield_strength`.
   - Write your findings to a file named `/home/user/top_features.txt` in exactly this format:
     ```
     defect_feature: <feature_name>
     yield_feature: <feature_name>
     ```

2. **Model Training and Evaluation**:
   - Split the dataset into training and testing sets. Use `test_size=0.2` and `random_state=42`. You must use all four sensor features as predictors.
   - **Classification**: Train a Logistic Regression model to predict `defect`. Use `sklearn.linear_model.LogisticRegression` with `random_state=42`. Calculate the accuracy score on the test set.
   - **Regression**: Train a Linear Regression model to predict `yield_strength`. Use `sklearn.linear_model.LinearRegression`. Calculate the Mean Squared Error (MSE) on the test set.
   - Write the evaluation metrics to a file named `/home/user/metrics.json` in exactly this format (round the values to 4 decimal places):
     ```json
     {
       "classification_accuracy": 0.1234,
       "regression_mse": 12.3456
     }
     ```

You will need to write and execute a Python script to accomplish this. All output files must be placed exactly at the specified paths.