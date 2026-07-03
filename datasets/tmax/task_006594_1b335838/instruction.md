You are a data scientist troubleshooting a pipeline. You have been given a dataset `/home/user/dataset.csv` containing several features and a target variable `y`. 

There is an existing Python script `/home/user/run_inference.py` that computes the exact analytical posterior mean for a Bayesian linear regression model (with an uninformative prior, effectively reducing to OLS). Currently, whenever you run this script on the dataset (if you copy `dataset.csv` to `cleaned_dataset.csv`), it fails with a `LinAlgError: Singular matrix` because the dataset contains a severe data quality issue (perfect collinearity). This is similar to a visualization script producing blank plots due to a misconfigured backend—the raw data is fundamentally incompatible with the naive math in the script.

Your task:
1. Identify the perfectly collinear feature in `/home/user/dataset.csv`.
2. Create a new file `/home/user/cleaned_dataset.csv` that is identical to `dataset.csv` but with the completely redundant feature removed. (If `fA` and `fB` are perfectly collinear, drop the one that appears later in the column order).
3. Run `python3 /home/user/run_inference.py`. The script is hardcoded to read `/home/user/cleaned_dataset.csv` and will output `/home/user/inference_results.json` containing the benchmarked inference time, the features used, and the computed model weights.
4. Ensure the resulting `/home/user/inference_results.json` successfully generates without errors.

Do not modify `/home/user/run_inference.py`. Use whatever combination of shell commands, Awk, Python, or other available tools you prefer to analyze the data and create the cleaned CSV.