You are an MLOps engineer tasked with evaluating different feature engineering strategies for predicting server failures, and tracking these experiments using MLflow.

Your task consists of the following steps:

1. **Environment & Server Setup**:
   - Install `mlflow`, `scikit-learn`, and `pandas`.
   - Start a local MLflow tracking server running on `http://127.0.0.1:5000` in the background. Ensure it stores its backend data in `/home/user/mlruns`.

2. **Data Preparation & Modeling**:
   - You have a dataset at `/home/user/telemetry.csv` containing server metrics: `cpu`, `mem`, `io`, and a binary target `failure`.
   - Write a Python script `/home/user/experiment.py` that reads this dataset.
   - Split the dataset into training and testing sets using `sklearn.model_selection.train_test_split` with `test_size=0.25` and `random_state=42`.
   - Set the MLflow tracking URI to your local server and set the experiment name to `Server_Failure_Predictor`.
   - Run three separate MLflow runs (within this experiment), each testing a different feature engineering pipeline using a `RandomForestClassifier(random_state=42)`. Do not scale the features. 
   - **Pipeline 1 ("baseline")**: Use the raw `cpu`, `mem`, and `io` columns.
   - **Pipeline 2 ("interactions")**: Use `sklearn.preprocessing.PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)` on the raw features.
   - **Pipeline 3 ("log_transform")**: Apply `numpy.log1p` to the raw features.
   
3. **Experiment Tracking**:
   - For each run, log the parameter `pipeline_name` (e.g., "baseline", "interactions", "log_transform").
   - Train the model on the training set, predict on the test set, and calculate the accuracy.
   - Log the metric `accuracy` to MLflow.
   - Log the trained model as an MLflow artifact named `rf_model`.

4. **Automated Reporting**:
   - After running the experiments, query the MLflow API (either via the Python client or REST API) to find the run with the highest `accuracy`.
   - Write the results to `/home/user/best_run.json` exactly in this format:
     ```json
     {
       "best_run_id": "<the_mlflow_run_id>",
       "best_pipeline": "<pipeline_name>"
     }
     ```

Ensure the MLflow server is still running at the end of your task so the verification script can inspect the tracked experiments.