You are a data scientist tasked with cleaning and processing a noisy dataset of sensor readings, then building a baseline predictive model. 

The dataset is located at `/home/user/sensor_data.csv`. It contains 50 continuous features (`sensor_1` through `sensor_50`), a `timestamp` column, and a binary target column `failure` (0 or 1). The dataset is highly imbalanced.

Perform the following pipeline:
1. **Tabular Transformation**: Drop the `timestamp` column. Standardize the 50 sensor features so that each has a mean of 0 and a standard deviation of 1.
2. **Sampling / Bootstrapping**: The `failure` class is the minority. Create a balanced dataset by upsampling the minority class using random resampling with replacement (bootstrapping) so that both classes have the exact same number of rows. Use a random seed of `42` for this sampling step.
3. **Dimensionality Reduction**: Apply Principal Component Analysis (PCA) to the standardized, balanced sensor features. Extract the top 5 principal components. Use a random seed of `42` for the PCA initialization if required by your library.
4. **Model Training and Evaluation**: Train a Logistic Regression model on these 5 principal components to predict the `failure` target. Use the same balanced dataset for training. (Do not perform a train/test split; evaluate on the training set for this baseline). Use a random seed of `42` for the Logistic Regression model.
5. **Reporting**: Calculate the sum of the explained variance ratio for the 5 principal components, and the ROC-AUC score of the model predictions.

Write a script in Python, R, or your preferred language to perform this pipeline.

Save your final results in a JSON file at `/home/user/pipeline_results.json` with the following exact keys:
- `"balanced_rows"`: (integer) The total number of rows in the balanced dataset.
- `"explained_variance_sum"`: (float) The sum of the explained variance ratio of the 5 PCA components, rounded to 4 decimal places.
- `"roc_auc"`: (float) The ROC-AUC score of the model on the training data, rounded to 4 decimal places.