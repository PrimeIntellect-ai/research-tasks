You are an ML Engineer preparing training data and building a reproducible baseline model for a new edge-device sensor system. 

A raw dataset is located at `/home/user/data/sensors.csv`. It contains sensor readings with columns: `temp`, `pressure`, `humidity`, and a binary label `target`.

Your task is to write a reproducible Python script at `/home/user/prepare_and_train.py` that performs the following pipeline:
1. **Dependencies**: Ensure your script or environment has `pandas` and `scikit-learn` installed.
2. **Feature Engineering**: Load the CSV and create two new features:
   - `temp_pressure_interaction`: the product of `temp` and `pressure`.
   - `high_humidity`: a binary feature which is `1` if `humidity` > 80.0, and `0` otherwise.
   Use the original features AND the two new features as your predictor set (5 features total).
3. **Reproducible Splitting**: Split the data into training and testing sets using `sklearn.model_selection.train_test_split` with `test_size=0.2` and `random_state=42`.
4. **Modeling**: Train a `sklearn.linear_model.LogisticRegression` model on the training data. You must initialize it with `random_state=42` to ensure pipeline reproducibility. Use default parameters otherwise.
5. **Evaluation**: Calculate the F1 score (using `sklearn.metrics.f1_score` with default parameters) of the model on the test set.
6. **Output**: Save the results to a JSON file at `/home/user/model_results.json` exactly in this format:
   ```json
   {
       "f1_score": <float>,
       "num_features": <int>
   }
   ```

Run your script to ensure the JSON file is created successfully.