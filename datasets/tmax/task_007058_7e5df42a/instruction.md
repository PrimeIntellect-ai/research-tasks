You are a data engineer building an ETL pipeline to process manufacturing sensor data. You have been given a dataset at `/home/user/sensor_data.csv` containing four columns: `id`, `sensor_A`, `sensor_B`, and `sensor_C`. 

Unfortunately, `sensor_C` has intermittent missing values (NaNs). Your task is to build a script that uses Bayesian inference to impute these missing values while also capturing the uncertainty of the predictions.

Please complete the following steps:
1. Create a shell script named `/home/user/run_etl.sh` that configures the numerical library environment for reproducibility and single-threaded execution. Specifically, it must export `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `MKL_NUM_THREADS=1`, and then execute your data processing script.
2. Write a data processing script (in any language of your choice, though Python with scikit-learn is recommended) that performs the following:
   - Loads `/home/user/sensor_data.csv`.
   - Separates the data into a training set (where `sensor_C` is not missing) and a prediction set (where `sensor_C` is missing).
   - Trains a Bayesian Ridge Regression model to predict `sensor_C` using `sensor_A` and `sensor_B`.
   - Performs hyperparameter tuning using 5-fold cross-validation (without shuffling) to find the best parameters. Search the following grid exactly:
     - `alpha_1`: [1e-2, 1e-4, 1e-6]
     - `alpha_2`: [1e-2, 1e-4, 1e-6]
     - `lambda_1`: [1e-2, 1e-4, 1e-6]
     - `lambda_2`: [1e-2, 1e-4, 1e-6]
   - Uses the negative mean squared error (`neg_mean_squared_error`) as the scoring metric for cross-validation.
   - Uses the best model found to predict the missing values of `sensor_C` and their standard deviations.
   - For rows where `sensor_C` was initially missing, fill `sensor_C` with the predicted mean, and record the predicted standard deviation in a new column called `sensor_C_std`.
   - For rows where `sensor_C` was not missing, keep the original `sensor_C` value and set `sensor_C_std` to exactly `0.0`.
   - Save the final dataset to `/home/user/imputed_sensor_data.csv` with columns: `id`, `sensor_A`, `sensor_B`, `sensor_C`, `sensor_C_std`. Ensure the rows are in the same order as the original file.
   - Save the best hyperparameters as a JSON file to `/home/user/best_params.json` (keys should be `alpha_1`, `alpha_2`, `lambda_1`, `lambda_2`).

Run your pipeline by executing `/home/user/run_etl.sh` so that the output files are generated.