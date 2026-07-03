You are a data scientist taking over a partially completed data pipeline. Your task is to fix a data leakage/typing issue, engineer a new feature, construct an inference script from raw model weights, and benchmark its performance.

Currently, we have a raw dataset at `/home/user/dataset.csv` and a JSON file containing trained logistic regression weights at `/home/user/model_weights.json`.

**Step 1: Data Cleaning & Feature Engineering**
Write a script to clean `/home/user/dataset.csv` and output it to `/home/user/cleaned_dataset.csv`.
- The dataset contains three columns: `id`, `value1`, and `value2`.
- `value1` has missing values. Fill them with `0.0`.
- `id` has missing values. When pandas loads this, it silently casts the `id` column to floats (e.g., `1.0` instead of `1`). Fill missing `id` values with `-1` and **ensure the `id` column is cast back to integer types**. 
- Engineer a new feature named `value3` which is the product of `value1` and `value2` (calculate this *after* filling missing values in `value1`).
- Save the result to `/home/user/cleaned_dataset.csv` (keep the columns in order: `id`, `value1`, `value2`, `value3`). Ensure `id` values are written as integers (no `.0`).

**Step 2: Model Architecture Reconstruction & Inference**
Write a Python script `/home/user/inference.py` to run predictions on the cleaned dataset.
- Read `/home/user/model_weights.json` which contains `"w1"`, `"w2"`, `"w3"`, and `"b"`.
- For each row, calculate the logit: `z = (w1 * value1) + (w2 * value2) + (w3 * value3) + b`.
- Calculate the probability: `p = 1 / (1 + exp(-z))`.
- The prediction is `1` if `p >= 0.5` else `0`.
- Output the results to `/home/user/predictions.csv` with exactly two columns: `id` (as integer) and `prediction` (as integer).

**Step 3: Numerical Accuracy Testing**
To test numerical stability and accuracy, calculate the sum of all probability values (`p`) across all rows. 
Save this exact sum, rounded to 4 decimal places, into `/home/user/accuracy.txt`.

**Step 4: Inference Performance Benchmarking**
Measure the time it takes to execute your `inference.py` script from the command line. Write a bash command or script that runs `inference.py` 100 times, calculates the average execution time in seconds, and appends the final average time to `/home/user/benchmark.txt` in the format `Average: X.XXXX seconds`. (It does not need to be precisely accurate, just an actual measurement).

Complete all steps and ensure the specified output files (`cleaned_dataset.csv`, `predictions.csv`, `accuracy.txt`, `benchmark.txt`) exist in `/home/user/` with the correct formats.