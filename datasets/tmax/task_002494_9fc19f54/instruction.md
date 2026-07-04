You are tasked with fixing and running a bash-based data evaluation pipeline. 

A previous data analyst left behind a pipeline to test a simple threshold-based classification model, but they misconfigured the evaluation script. It currently outputs empty strings or invalid calculations. 

Here is the current state of your workspace:
- `/home/user/data.csv`: A dataset with columns `id,score,label` (where label is 0 or 1).
- `/home/user/predict.sh`: A model script. Usage: `./predict.sh <threshold> <input_csv>` outputs `id,prediction` to stdout.
- `/home/user/evaluate.awk`: An AWK script designed to take a joined CSV of `id,score,label,prediction` and compute the prediction accuracy (between 0.0 and 1.0). Currently, it contains logical bugs (e.g., incorrect field separators and failing to skip the header).

Your objectives:
1. **Fix the Evaluation Script**: Debug and fix `/home/user/evaluate.awk` so that it correctly computes the accuracy of predictions. It should print a single float representing the accuracy.
2. **Reproducible Pipeline & Hyperparameter Tuning**: Write a bash script `/home/user/run_pipeline.sh` that:
   - Iterates through the threshold values: `10, 20, 30, 40, 50`.
   - For each threshold, runs `./predict.sh` on `data.csv`.
   - Joins the output of `predict.sh` with the original `data.csv` based on the `id` column.
   - Passes the joined data to your fixed `evaluate.awk` to compute the accuracy.
   - Measures the inference time (the execution time of `./predict.sh`) in milliseconds for each run.
3. **Save Results**: 
   - Write the summary of all runs to `/home/user/tuning_results.csv` with the header `threshold,accuracy,time_ms`.
   - Determine the threshold that yields the highest accuracy and write JUST the integer value of that optimal threshold to `/home/user/best_threshold.txt`. If there is a tie, pick the lower threshold.

Constraints:
- You must use Bash and standard Linux utilities (like `awk`, `join`, `sed`, `date`, etc.). Python/R are not allowed.
- Assume `predict.sh` is a black-box model. Do not modify it.