You are an MLOps engineer tasked with setting up a lightweight, Bash-based experiment tracking and inference benchmarking pipeline.

First, you need to install `datamash` to help with aggregation. We have vendored the source code for GNU `datamash` 1.8 at `/app/datamash-1.8`. However, a previous engineer accidentally introduced a bug in the `Makefile.in` (or configuration) that causes the build to fail (a deliberate perturbation related to a missing or broken compiler flag / syntax). You must fix this perturbation, compile, and install `datamash` so it is available in your PATH.

Second, you must implement the primary evaluation script. Write a Bash script at `/home/user/eval_tracker.sh`. 
This script will be used to process multi-source inference logs, track experiment performance, and benchmark inference times. 

The script must accept exactly one argument: the path to a CSV file containing inference logs.
The input CSV has no header and contains 5 columns:
1. `log_id` (string)
2. `experiment_id` (string)
3. `inference_time_ms` (float)
4. `ground_truth` (integer)
5. `prediction` (integer or empty)

Your script must perform the following:
1. Filter out any rows where the `prediction` column is strictly empty (missing).
2. For each `experiment_id`, calculate:
   - The average `inference_time_ms` (rounded to 4 decimal places).
   - The accuracy (number of rows where `ground_truth` == `prediction` divided by the total valid rows for that experiment, rounded to 4 decimal places).
3. Output the results in a comma-separated format: `experiment_id,avg_inference_time,accuracy`.
4. The output must be sorted alphabetically by `experiment_id`.

Example Input:
```
log1,expA,12.5,1,1
log2,expA,15.0,0,1
log3,expB,10.0,1,
log4,expB,11.2,1,1
```

Example Output:
```
expA,13.7500,0.5000
expB,11.2000,1.0000
```

Constraints:
- You must use standard shell utilities and the fixed `datamash` tool.
- Do NOT use Python, Perl, or other high-level scripting languages for the evaluation script. Use Bash, awk, datamash, sed, etc.
- Make sure your script handles arbitrary valid CSVs following the schema. An automated system will fuzz your script against a hidden reference oracle to ensure absolute bit-exact equivalence.