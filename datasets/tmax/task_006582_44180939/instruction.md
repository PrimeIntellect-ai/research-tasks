You are a data engineer tasked with building a predictive ETL pipeline. 

You have been provided with a historical dataset of system metrics located at `/home/user/historical_data.csv` (which has feature columns `x1` through `x5` and a target column `y`). You also have a new incoming batch of data at `/home/user/new_batch.csv` (which only contains the feature columns `x1` through `x5`).

Your task is to build a mathematical modeling and inference pipeline. You may use any programming language, but you will likely need to install appropriate dependencies (e.g., `scikit-learn`, `pandas` if using Python).

Perform the following steps:
1. **Cross-validation and Hyperparameter Tuning**: 
   Train an `ElasticNet` regression model on `/home/user/historical_data.csv`. You must use 5-fold cross-validation (`GridSearchCV` if using Python/scikit-learn) to find the best hyperparameters from the following grid:
   - `alpha`: `[0.1, 1.0, 10.0]`
   - `l1_ratio`: `[0.1, 0.5, 0.9]`
   Ensure you set any random seeds for the model to `42` (e.g., `random_state=42`) to ensure reproducibility.
2. **Model Persistence**: 
   Save the trained model with the best hyperparameters to disk at `/home/user/best_model.pkl`.
3. **Inference and Benchmarking**: 
   Load the saved model and perform inference on `/home/user/new_batch.csv`. 
   You must benchmark the total inference time for predicting the new batch.
4. **Reporting**: 
   Create a JSON summary report at `/home/user/pipeline_results.json` with the following exact keys:
   - `"best_alpha"`: The optimal `alpha` value found (float).
   - `"best_l1_ratio"`: The optimal `l1_ratio` value found (float).
   - `"cv_best_score"`: The best mean cross-validated score (R-squared), rounded to 4 decimal places (float).
   - `"first_5_predictions"`: A list of the first 5 prediction values for the new batch, each rounded to 4 decimal places.
   - `"inference_time_seconds"`: The time taken to run the predictions on the new batch (float).

You will need to ensure any necessary packages (e.g., `scikit-learn`, `pandas`) are installed in your environment before running your scripts.