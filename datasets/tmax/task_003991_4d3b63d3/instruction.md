I am a researcher organizing a messy dataset of environmental sensor readings to predict crop yield. The dataset is located at `/home/user/sensor_data.csv`. I need you to set up an analysis environment, clean the features, engineer a new one, and train a baseline model to see how predictable the yield is.

Please perform the following steps:

1. **Environment Setup**: You will need to install the necessary libraries (e.g., pandas, scikit-learn, numpy) using your preferred language and package manager.
2. **Correlation and Covariance Analysis**: The dataset contains some redundant sensors. Calculate the Pearson correlation matrix for all features (excluding the target variable, `yield`). Find any pairs of features that have an absolute correlation greater than `0.85`. For each highly correlated pair, drop the feature that has the *lower variance* across the dataset. Keep the one with the higher variance.
3. **Feature Engineering**: Create a new feature named `temp_humid_idx` which is the product of the `temperature` and `humidity` columns. Add this to your modeling features.
4. **Cross-Validation and Hyperparameter Tuning**: 
   - Target variable: `yield`
   - Features: `temperature`, `humidity`, `temp_humid_idx`, and the remaining sensors after step 2.
   - Model: Ridge Regression.
   - Tuning: Use Grid Search with 5-fold Cross-Validation (do **not** shuffle the data during CV to ensure deterministic results).
   - Hyperparameter grid to search: `alpha` in `[0.1, 1.0, 10.0]`.
   - Scoring metric: R-squared ($R^2$).
5. **Reporting**: Generate a JSON file at `/home/user/analysis_results.json` containing the exact following keys:
   - `"dropped_features"`: A list of strings containing the exact column names dropped during step 2.
   - `"best_alpha"`: The best alpha value found by the grid search (float).
   - `"best_cv_score_r2"`: The mean cross-validation R-squared score of the best model, rounded to 4 decimal places (float).

Ensure the final JSON is perfectly formatted. You may use any programming language (Python is recommended) to complete this task.