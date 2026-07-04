You are a data analyst tasked with processing machine sensor data to understand failure modes.

A raw dataset is located at `/home/user/sensor_data.csv` with the following columns:
- `id`: Machine ID
- `temperature`: Operating temperature
- `vibration`: Vibration level
- `rotation_speed`: Rotation speed in RPM
- `failed`: Target variable (1 if the machine failed, 0 otherwise)

Please write and execute a Python script to perform the following analysis pipeline:

1. **Feature Engineering**: Create a new feature called `temp_vib_ratio` which is calculated as `temperature / vibration`.
2. **Hypothesis Testing**: Perform a Welch's t-test (independent two-sample t-test with unequal variances) to compare the `temp_vib_ratio` between machines that failed (`failed == 1`) and machines that did not fail (`failed == 0`). Note the resulting p-value.
3. **Classification & Cross-Validation**: Train a Random Forest Classifier to predict the `failed` status using the features: `temperature`, `vibration`, `rotation_speed`, and `temp_vib_ratio`.
   - Set `random_state=42` for the Random Forest model.
   - Use `GridSearchCV` to perform 3-fold cross-validation to find the optimal `max_depth` hyperparameter.
   - Test the following `max_depth` values: `[3, 5, None]`.
   - Use standard accuracy as your scoring metric.

Write your final extracted metrics to a JSON file at `/home/user/analysis_report.json`. The JSON file must contain exactly these keys:
- `"p_value"`: (float) The p-value from the Welch's t-test.
- `"best_max_depth"`: (integer or null) The best `max_depth` parameter found by GridSearchCV.
- `"best_cv_accuracy"`: (float) The `best_score_` attribute from the fitted GridSearchCV.

You may install any standard data science libraries (like pandas, scipy, and scikit-learn) via pip if they are not already installed.