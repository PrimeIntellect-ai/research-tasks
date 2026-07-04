You are an MLOps engineer tasked with building an end-to-end ETL pipeline, training a classification model, and tracking the experiment artifacts locally.

You have been provided with raw sensor data (which will be located at `/home/user/sensor_data.csv` once you begin). 

Your objective is to write and execute a Python pipeline that performs the following steps exactly:

1. **Dependency Installation**: Install `pandas`, `scikit-learn`, and `mlflow`.
2. **ETL Pipeline**: 
   - Load `/home/user/sensor_data.csv`.
   - The dataset contains features `sensor_1` through `sensor_5`, and a binary `target` column.
   - Impute any missing values in the `sensor_3` column using the median of that column.
   - Scale all feature columns (`sensor_1` to `sensor_5`) using scikit-learn's `StandardScaler`.
3. **Classification & Experiment Tracking**:
   - Split the processed data into training and testing sets (80% train, 20% test) using `train_test_split` with `random_state=42`.
   - Configure `mlflow` to use a local tracking URI: `file:///home/user/mlruns`.
   - Create an MLflow experiment named `Sensor_Failure_Exp`.
   - Within an MLflow run under this experiment:
     - Train a `RandomForestClassifier` with `n_estimators=50`, `max_depth=5`, and `random_state=42`.
     - Log the parameter `n_estimators` to MLflow.
     - Calculate the accuracy on the test set and log it as a metric named `test_accuracy`.
     - Log the scikit-learn model as an artifact named `rf_model`.
     - Set an MLflow tag for the run: `pipeline_version` with the value `v1.0`.
4. **Numerical Accuracy Testing**:
   - Save the exact test accuracy you calculated to a file located at `/home/user/test_results.json`. The file must be valid JSON in the format: `{"test_accuracy": 0.1234}` (replacing 0.1234 with your actual float value).

Ensure all scripts are run and the `/home/user/mlruns` directory and `/home/user/test_results.json` file are correctly populated before completing the task.