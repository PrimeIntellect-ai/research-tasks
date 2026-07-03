You are tasked with fixing and completing an automated machine learning ETL and validation pipeline. 

A previous data scientist left behind a partially completed script `/home/user/pipeline.py` and a dataset `/home/user/sensor_data.csv`. The script is supposed to clean the dataset, train a classification model, log validation metrics, and generate a feature importance plot. However, it currently crashes, the data cleaning logic is missing, and the visualization attempts to open a GUI window which fails in our headless server environment.

Your objectives are:

1. **Fix the ETL logic**: In `/home/user/pipeline.py`, complete the `clean_data(df)` function. It must:
   - Impute missing values in the `temperature` and `vibration` numeric columns using the **median** of each column.
   - Perform One-Hot Encoding on the categorical column `sensor_type` (drop the original `sensor_type` column and include the new one-hot encoded columns).
   - Ensure the target column `failure` remains unchanged.
   - Return the cleaned pandas DataFrame.

2. **Fix the Plotting Misconfiguration**: The `plot_feature_importance()` function attempts to use `plt.show()`, which crashes in headless environments. Fix the script so it uses the `Agg` matplotlib backend. Modify the function to save the plot as `/home/user/importance.png` instead of attempting to display it.

3. **Complete Model Validation**: Modify `train_and_evaluate()` to calculate the `accuracy` and `f1_score` (macro average) on the test set. Save these metrics as a JSON file at `/home/user/metrics.json` with the exact keys: `"accuracy"` and `"f1_score"`.

4. **Write a Unit Test**: Create a test file `/home/user/test_pipeline.py` using `pytest`. Write at least one test named `test_clean_data` that creates a small mock DataFrame with missing numeric values and categorical strings, passes it through your `clean_data()` function from `pipeline.py`, and asserts that the output contains no null values and successfully one-hot encodes the categorical column.

You will need to install any missing python dependencies (e.g., pandas, scikit-learn, matplotlib, pytest) into the user environment. Ensure that running `python /home/user/pipeline.py` executes successfully from start to finish without errors, outputs the image, and writes the JSON metrics. Finally, ensure that running `pytest /home/user/test_pipeline.py` passes successfully.