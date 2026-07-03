You are an MLOps engineer tasked with building a reproducible, tracked machine learning pipeline. 

Your objective is to set up the analysis environment, manage local artifact storage, perform cross-validation with hyperparameter tuning, and validate the model's outputs.

The raw data has been provided at `/home/user/data/raw.csv`. It contains 10 feature columns (`feature_0` to `feature_9`) and a `target` column.

Please perform the following steps:

1. **Environment Setup**:
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `pandas`, `numpy`, `scikit-learn`, and `joblib`.

2. **Storage Management**:
   - Create a structured local artifact registry with the following exact directory paths:
     - `/home/user/artifacts/models`
     - `/home/user/artifacts/metrics`
     - `/home/user/artifacts/predictions`

3. **Pipeline Implementation**:
   - Write a Python script at `/home/user/train.py` that accomplishes the following:
     - Loads the dataset from `/home/user/data/raw.csv`.
     - Splits the data into a training set (80%) and a hold-out test set (20%). You MUST use `random_state=42` for the split. Do not shuffle the data before splitting (use `shuffle=False` to ensure deterministic indices).
     - Uses `scikit-learn`'s `Ridge` regression model.
     - Performs 5-fold cross-validation (`GridSearchCV` with `cv=5`) on the training set to find the best `alpha` hyperparameter from this list: `[0.1, 1.0, 10.0, 100.0]`. Use negative mean squared error as the scoring metric.
     - Saves the best trained model using `joblib` to `/home/user/artifacts/models/best_ridge.pkl`.
     
4. **Model Output Validation**:
   - In the same `train.py` script, evaluate the best model on the hold-out test set.
   - Calculate the Mean Squared Error (MSE) on the test set and write this single float value (rounded to 4 decimal places) to `/home/user/artifacts/metrics/mse.txt`.
   - Generate predictions for the test set. Save these predictions to `/home/user/artifacts/predictions/preds.csv`. The CSV must contain exactly two columns: `index` (the original integer index from the pandas DataFrame of the test set) and `prediction` (the predicted float value). Do not include an extra unnamed index column.

Execute your script to ensure all artifacts are successfully generated in their respective directories.