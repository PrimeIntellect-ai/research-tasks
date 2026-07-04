You are an MLOps engineer responsible for evaluating experiment artifacts from a machine learning pipeline. You need to write a Bash script that analyzes prediction outputs, tests for pipeline reproducibility (verifying dimensionality reduction features haven't drifted), and computes classification accuracy along with confidence intervals using only standard Linux shell utilities (like `awk`, `bc`, `sed`, `grep`).

Create a Bash script at `/home/user/evaluate_experiments.sh` that takes exactly two arguments:
1. Path to the baseline model's CSV artifact (e.g., `/home/user/baseline.csv`)
2. Path to the new model's CSV artifact (e.g., `/home/user/new_model.csv`)

Both CSV files will have a header row and follow this schema:
`id,true_label,pred_label,pca1,pca2`
- `true_label`: The actual class (0 or 1)
- `pred_label`: The predicted class (0 or 1)
- `pca1`, `pca2`: Dimensionality reduction feature coordinates used for the prediction

Your script must perform the following:

**1. Reproducibility Check**
Verify that the `pca1` and `pca2` columns (columns 4 and 5) for every corresponding `id` are perfectly identical between the two files. 
- If they differ for *any* row (excluding the header), your script must print exactly `Reproducibility Error` to standard output and exit immediately with status code `1`.

**2. Classification Metrics & Hypothesis Testing**
If the files are reproducible, calculate the classification accuracy (where `true_label == pred_label`) for both the baseline and the new model.
Also, calculate the 95% Confidence Interval for the **baseline model's** accuracy using the normal approximation:
- Standard Error (SE) = `sqrt( accuracy * (1 - accuracy) / n )`
- Lower Bound = `accuracy - (1.96 * SE)`
- Upper Bound = `accuracy + (1.96 * SE)`
*(where `n` is the total number of data rows, excluding the header).*

**3. Reporting**
If the reproducibility check passes, your script must save a report to `/home/user/experiment_report.txt` in exactly this format, with all numerical values rounded to exactly 4 decimal places (e.g., `0.8000`):

```
Baseline Accuracy: <value>
Baseline CI: [<lower_bound>, <upper_bound>]
New Model Accuracy: <value>
```
After generating the report, the script should exit with status code `0`.

Ensure your script is executable (`chmod +x`). You must implement the math using bash utilities like `awk` or `bc` with sufficient precision before rounding.