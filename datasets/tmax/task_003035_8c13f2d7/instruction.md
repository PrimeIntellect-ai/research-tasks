You are a Machine Learning Engineer responsible for preparing an automated testing pipeline for a newly developed model.

We have a Python training script located at `/home/user/train_and_plot.py`. This script takes a random seed as a command-line argument, generates synthetic training data, trains a Logistic Regression model, creates a plot of the decision boundary, saves it to `plot.png`, and prints the final model accuracy to standard output. 

Unfortunately, the script is currently failing to run in our headless CI environment. It crashes due to a `matplotlib` backend misconfiguration (it attempts to open a GUI window).

Your tasks are:

1. **Environment Setup & Bug Fix**: Fix the environment or the execution method so that `/home/user/train_and_plot.py` runs successfully in this headless terminal without removing or commenting out the plotting code in the Python script.

2. **Pipeline Scripting (Bash)**: Write a Bash script at `/home/user/run_eval.sh`. This script must:
   - Loop 30 times, executing the Python script with seeds `1` through `30` (e.g., `python /home/user/train_and_plot.py 1`, `python /home/user/train_and_plot.py 2`, etc.).
   - Capture the accuracy score printed by the script for each run.

3. **Hypothesis Testing & Aggregation**: Inside your Bash script (`run_eval.sh`), compute the following statistics based on the 30 accuracy scores:
   - **Mean Accuracy**
   - **Sample Standard Deviation** (divide by N-1)
   - **95% Confidence Interval Margin of Error** using the formula: `1.96 * (sample_std_dev / sqrt(30))`
   - Evaluate a hypothesis: We want to be 95% confident that the true accuracy is greater than `0.80`. Check if `(Mean Accuracy - Margin of Error) > 0.80`.

   *Note: You may use `awk`, `bc`, or an inline `python -c` command within your Bash script to perform these mathematical calculations, but the core pipeline logic and execution must be in Bash.*

4. **Reporting**: Your `run_eval.sh` script must ultimately write the final results to `/home/user/metrics.json` strictly in the following JSON format:
```json
{
  "mean_accuracy": 0.0000,
  "margin_of_error": 0.0000,
  "hypothesis_passed": true
}
```
*(Round the float values to 4 decimal places, e.g., 0.8532)*

Make sure `/home/user/run_eval.sh` is executable (`chmod +x`). 
When you are done, run your `/home/user/run_eval.sh` script to generate the `metrics.json` file.