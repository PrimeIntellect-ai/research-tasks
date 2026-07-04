You are a data engineer tasked with building an ETL and modeling pipeline for a set of IoT sensor logs.

You have a raw log file located at `/home/user/raw_logs.txt`. The file contains space-separated values with the following columns:
1. `timestamp` (ISO-8601 string)
2. `sensor_id` (string)
3. `status` (string: "OK" or "ERR")
4. `temperature` (float)
5. `vibration` (float)
6. `failure_label` (integer: 0 or 1)

Please perform the following steps to complete the pipeline:

1. **Data Extraction (Bash/AWK):** 
   Write a shell script or command to process `/home/user/raw_logs.txt`. Filter out any rows where the `status` is "ERR". Extract only the `timestamp`, `temperature`, `vibration`, and `failure_label` columns. Save the result as a comma-separated values (CSV) file at `/home/user/clean_data.csv`. The file must include a header row exactly as follows: `ts,temp,vibration,failure`.

2. **Feature Engineering & Modeling (Python):**
   Write a Python script that reads `/home/user/clean_data.csv`. 
   - Engineer a new feature called `temp_vibe_ratio` which is calculated as `temp / vibration`.
   - Define your feature matrix `X` using the columns `temp`, `vibration`, and `temp_vibe_ratio`. Define your target `y` as `failure`.
   - Initialize a `DecisionTreeClassifier` from `sklearn.tree` with `random_state=42`.
   - Perform hyperparameter tuning using `GridSearchCV` from `sklearn.model_selection` with 3-fold cross-validation (`cv=3`). Search over the `max_depth` parameter with the values `[2, 3, 4, 5]`.

3. **Reporting:**
   After finding the best model via grid search, write the results to a JSON file at `/home/user/metrics.json`. The JSON file must have exactly this format:
   ```json
   {
       "best_depth": <integer>,
       "best_cv_score": <float rounded to 3 decimal places>
   }
   ```

Complete all steps and ensure `/home/user/metrics.json` is generated with the correct tuning results.