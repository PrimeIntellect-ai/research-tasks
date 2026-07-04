You are a bioinformatics analyst tasked with evaluating a sequence scoring pipeline. A colleague has created a Jupyter notebook that generates pseudo-alignment scores for k-mers, but the downstream processing pipeline currently fails due to numerical stability issues when calculating the population variance of these scores.

Your task is to build a robust bash orchestrator script that runs the notebook, processes its output to calculate the variance stably, and verifies the result against a reference dataset.

Here are your instructions:
1. Create a bash script at `/home/user/orchestrate_pipeline.sh`.
2. The script must first execute the existing Jupyter notebook located at `/home/user/generate_scores.ipynb` in place. You should use `jupyter nbconvert` or `papermill` to execute it. This notebook reads an internal sequence dataset and outputs a list of floating-point scores to `/home/user/raw_scores.txt` (one score per line).
3. The scores generated are very large and highly clustered (e.g., around $10^9$). A naive one-pass variance calculation ($\frac{\sum x^2}{N} - \mu^2$) will fail due to catastrophic cancellation (floating-point precision loss). 
4. In your bash script, use `awk` to parse `/home/user/raw_scores.txt` and calculate the **population variance** of the scores using a numerically stable algorithm (such as Welford's method or a two-pass mean-centered algorithm).
5. Output the calculated variance as a single floating-point number to `/home/user/calculated_variance.txt` (formatted to 6 decimal places, e.g., `0.000688`).
6. Compare your calculated variance to the reference variance stored in `/home/user/reference_variance.txt`. If the absolute difference is less than `0.0001`, your script must write the exact string `PASS` to `/home/user/pipeline_status.log`. Otherwise, write `FAIL`.

Ensure your script is executable and performs all the steps sequentially when run. 

*Note: You do not need to modify the Jupyter notebook itself. All logic for the stable mathematical calculation and comparison must be handled in your Bash orchestrator script.*