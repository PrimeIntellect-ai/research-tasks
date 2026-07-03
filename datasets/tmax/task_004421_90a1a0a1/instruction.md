You are an analyst tasked with building an automated experiment tracking pipeline for evaluating models on dirty data.

You have been provided with a directory of CSV files located at `/home/user/datasets/`. Each file contains three feature columns (`feature1`, `feature2`, `feature3`) and one `target` column. The data contains missing values and extreme outliers.

Your goal is to write a Python script that processes a single dataset, and a Bash script that orchestrates the processing of all datasets and logs the results.

Step 1: Write a Python script `/home/user/evaluate.py` that takes a dataset file path as a command-line argument and performs the following:
1. Load the CSV file.
2. **Missing value handling**: Fill any missing values in `feature1`, `feature2`, and `feature3` with the median of their respective columns.
3. **Outlier handling**: Remove any rows where the `target` value is less than or equal to the 1st percentile, or greater than or equal to the 99th percentile of the `target` column.
4. **Cross-validation and hyperparameter tuning**: Use `sklearn.linear_model.Ridge`. Perform grid search using 3-fold cross-validation (without shuffling) to find the best `alpha` among `[0.1, 1.0, 10.0]`. Optimize for the negative mean absolute error (MAE).
5. Print out the best `alpha` and its corresponding cross-validated MAE (as a positive number, rounded to 3 decimal places) in the format: `best_alpha,best_mae`.

Step 2: Write a Bash script `/home/user/run_experiments.sh` that:
1. Iterates over all `.csv` files in `/home/user/datasets/` in alphabetical order.
2. Calls `evaluate.py` for each file.
3. Tracks the experiments by appending the results to `/home/user/experiment_log.csv`. 
4. The output `/home/user/experiment_log.csv` must have the header `dataset,best_alpha,best_mae` and each subsequent line should contain the base filename (e.g., `data_A.csv`) followed by the output of the Python script.

Make sure your bash script creates or overwrites the log file with the header before starting the loop. Run your bash script to generate the final `/home/user/experiment_log.csv`.