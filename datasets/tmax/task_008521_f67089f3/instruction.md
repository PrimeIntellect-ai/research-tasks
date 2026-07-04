You are a data scientist taking over a machine learning project. The previous data scientist wrote a data processing and modeling pipeline, but there are issues with data types, and they left before implementing proper cross-validation and testing.

You have a dataset located at `/home/user/data/dataset.parquet`. 
There is an existing script at `/home/user/pipeline.py` containing three functions: `load_data()`, `clean_data(df)`, and `train_and_evaluate(df)`.

Currently, the `clean_data(df)` function replaces missing values in the `user_id` column with `np.nan`. Because `user_id` contains large integers, Pandas silently casts the entire column to `float64`, causing a loss of precision that degrades model performance downstream. 

Your tasks are:
1. **Fix the Data Pipeline**: Modify `clean_data(df)` in `/home/user/pipeline.py` so that it uses Pandas' nullable integer data type (`'Int64'`) for the `user_id` column. Missing values should be represented as `pd.NA` so the column remains an integer type and avoids the silent float cast.
2. **Implement Cross-Validation & Hyperparameter Tuning**: Modify the `train_and_evaluate(df)` function. Instead of a simple train/test split, use `GridSearchCV` from `scikit-learn` with a `HistGradientBoostingClassifier`. 
   - Use 3-fold cross-validation (`cv=3`).
   - Use the following parameter grid: `max_iter`: [50, 100], `learning_rate`: [0.05, 0.1].
   - Ensure you use `random_state=42` for the classifier.
3. **Experiment Tracking**: At the end of `train_and_evaluate(df)`, save a JSON file to `/home/user/experiment_results.json` containing the best parameters and the best cross-validation score. The JSON must have the following exact structure:
   ```json
   {
     "best_params": {
       "learning_rate": <float>,
       "max_iter": <int>
     },
     "best_score": <float>
   }
   ```
4. **Write a Test**: Create a test file at `/home/user/test_pipeline.py`. Write a `pytest` compatible test function named `test_no_float_cast()` that:
   - Calls `load_data()` and `clean_data()`.
   - Asserts that the `user_id` column's dtype in the cleaned dataframe is explicitly `'Int64'`.
   - Asserts that there are no `float64` types in the `user_id` column.

You will need to install any necessary requirements (like `pandas`, `scikit-learn`, `pytest`, `pyarrow`). Do not change the random state or data generation logic in `load_data()`.