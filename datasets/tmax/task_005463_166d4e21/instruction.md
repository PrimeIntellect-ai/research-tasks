You are an MLOps engineer tasked with analyzing a set of model experiment artifacts. 
In the directory `/home/user/experiments/`, there are several CSV files (e.g., `exp_01.csv`, `exp_02.csv`). Each file contains the predictions of a machine learning model across different experiment runs.

The CSV files contain the following columns:
- `run_id`: A string identifier for the experiment run.
- `y_true`: The ground truth binary label (0 or 1).
- `y_pred`: The predicted binary label (0 or 1).
- `confidence`: The model's predicted probability or confidence score (float between 0.0 and 1.0).

Your task is to write a Python script that processes these files, performs model output validation, and uses Bayesian inference to estimate the true accuracy of the valid runs.

**Step 1: Aggregation and Validation**
For each unique `run_id` across all files, calculate:
1. **Accuracy**: The proportion of rows where `y_true == y_pred`.
2. **Mean Confidence**: The average of the `confidence` column.

A run should be **flagged** (considered invalid) if it meets **either** of these conditions:
- The Accuracy is strictly less than 0.60.
- The absolute difference between Accuracy and Mean Confidence is strictly greater than 0.15 (indicating severe miscalibration).

**Step 2: Bayesian Inference**
For all the rows belonging to **unflagged (valid) runs**, we want to estimate the global true success rate (accuracy).
Model the overall accuracy using a Binomial likelihood and a Beta conjugate prior.
Assume a prior Beta distribution with parameters $\alpha_0 = 2$ and $\beta_0 = 2$.
Calculate the parameters of the posterior Beta distribution ($\alpha_{post}$ and $\beta_{post}$) using the aggregated successes (where `y_true == y_pred`) and failures (where `y_true != y_pred`) from all valid runs combined.

**Step 3: Output generation**
Create a JSON file at `/home/user/results.json` containing the results. The JSON must exactly match this structure:
```json
{
  "flagged_runs": ["run_X", "run_Y"],
  "posterior_alpha": 123,
  "posterior_beta": 45
}
```
*Note: The `flagged_runs` list must be sorted alphabetically.*

Please execute the necessary code to generate the final `/home/user/results.json` file.