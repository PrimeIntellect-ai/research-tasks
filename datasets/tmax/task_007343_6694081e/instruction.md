You are an AI assistant helping a researcher organize their datasets and fix a buggy machine learning pipeline. 

The researcher has two datasets:
1. `/home/user/data/measurements.csv` - Contains columns `id`, `sensor_A`, `sensor_B`, `sensor_C` (with some missing values).
2. `/home/user/data/targets.csv` - Contains columns `id`, `target`.

Currently, the researcher has a script `/home/user/model.py` that merges these datasets, imputes missing values, scales the features, engineers a new feature, and trains a model. However, the script suffers from **data leakage**: it calculates imputation statistics and scaling parameters on the *entire* dataset before splitting into train and test sets. 

Your task is to rewrite the machine learning pipeline (you can edit `/home/user/model.py` or write a new script) to follow proper practices and prevent data leakage. Specifically, you must:

1. **Multi-source joining**: Merge `measurements.csv` and `targets.csv` on `id`.
2. **Feature engineering**: Create a new feature `sensor_ratio` = `sensor_A` / `sensor_B`.
3. **Data Splitting**: Split the merged data into features (`sensor_A`, `sensor_B`, `sensor_C`, `sensor_ratio`) and the target (`target`). Use an 80/20 train-test split with `random_state=42` using `sklearn.model_selection.train_test_split`.
4. **Missing value handling**: Impute any missing values (NaNs) in the features using the **mean** of the respective columns from the *training set only*. Apply these imputation values to both train and test sets.
5. **Scaling**: Standardize the features (zero mean, unit variance) using the statistics calculated *only* from the training set. (You can use `sklearn.preprocessing.StandardScaler` or compute manually).
6. **Correlation Analysis**: Calculate the Pearson correlation coefficient between the *unscaled, but imputed* `sensor_ratio` feature and the `target` strictly within the training set.
7. **Modeling**: Train a `sklearn.linear_model.Ridge` regression model (with `alpha=1.0`) on the scaled training features and evaluate its $R^2$ score on the scaled test features.
8. **Experiment Tracking**: Save the final results to a JSON file at `/home/user/experiment_results.json`. The JSON file must have exactly two keys:
   - `"train_ratio_correlation"`: The float value of the correlation calculated in step 6.
   - `"test_r2_score"`: The float value of the $R^2$ score on the test set.

Ensure your pipeline strictly avoids data leakage. Output the JSON file directly. Do not change the random state or split proportions.