You are a data scientist working for a manufacturing company. You need to prepare a pipeline that cleans IoT sensor data, merges it with maintenance records, trains a predictive maintenance model, and benchmarks its inference performance.

Your environment is an empty Linux machine. You may use any programming language, but you will likely need to install necessary packages (e.g., pandas, scikit-learn for Python) first.

Here are your instructions:

1. **Data Joining & Cleaning**
   - You have two datasets: `/home/user/data/sensors.csv` (contains `machine_id`, `temperature`, `vibration`) and `/home/user/data/maintenance.json` (contains `machine_id`, `needs_repair`).
   - Merge the two datasets on `machine_id`.
   - The `temperature` column contains missing values (represented as empty strings or nulls). Impute these missing values using a bootstrap sampling method: for every missing value, draw a random sample (with replacement) from the *non-null* temperature values in the dataset. Use a fixed random seed of `42` for this sampling process to ensure reproducibility.
   - Save the fully merged and cleaned dataset to `/home/user/results/cleaned_data.csv`.

2. **Classification Modeling**
   - Using the cleaned dataset, train a Random Forest Classifier to predict `needs_repair` (target) using `temperature` and `vibration` (features).
   - Use default hyperparameters but set the random state/seed to `42`.
   - Calculate the accuracy of the model on the *entire* training dataset.

3. **Inference Benchmarking**
   - Benchmark the inference speed of your trained model.
   - Run the `predict` method on the entire cleaned dataset 100 times in a loop.
   - Calculate the average time it takes for a single full-dataset prediction pass, in milliseconds.

4. **Reporting**
   - Create a JSON report at `/home/user/results/summary.json` with exactly the following keys:
     - `"num_rows_cleaned"`: The integer number of rows in the final cleaned dataset.
     - `"model_accuracy"`: The accuracy of the model on the dataset, rounded to 2 decimal places (e.g., 0.95).
     - `"avg_inference_ms"`: The average time for one full-dataset prediction pass (in milliseconds) over the 100 runs, as a float.

Ensure all output directories exist before writing to them.