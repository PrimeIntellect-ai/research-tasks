You are an MLOps engineer tasked with analyzing artifact logs from an A/B test of two model versions. The system logged inference latencies to `/home/user/inference_logs.csv`. However, the telemetry system sometimes drops values, records negative values due to clock sync issues, or records massive outliers during cold starts.

Your objective is to write a Bash script `/home/user/pipeline.sh` that orchestrates data cleaning and statistical analysis to evaluate the latency difference between Model A and Model B. You may use standard Unix tools (awk, sed) or create a Python script invoked by your Bash script for the math.

Here is the step-by-step requirement for `/home/user/pipeline.sh`:

1. **Missing Value and Sanity Cleaning:**
   Read `/home/user/inference_logs.csv` (Headers: `req_id,model,latency`). Filter out any rows where `latency` is `NA`, empty, or less than 0.

2. **Outlier Handling (Per Model):**
   For both Model A and Model B separately, calculate the First Quartile (Q1) and Third Quartile (Q3) of the cleaned latencies. (Use the standard definition of quartiles where you interpolate if necessary, e.g., `numpy.percentile(..., 25)`). 
   Remove any rows where the latency is strictly less than `Q1 - 1.5 * IQR` or strictly greater than `Q3 + 1.5 * IQR`.

3. **Sampling and Bootstrap Methods:**
   Using the outlier-free datasets, perform a bootstrap analysis to find the 95% confidence interval for the difference in means: `Mean(Model B) - Mean(Model A)`.
   - Use exactly 10,000 bootstrap iterations.
   - For reproducibility in testing, if you use Python for this step, you MUST set `numpy.random.seed(42)` before generating your bootstrap samples. 
   - Each bootstrap iteration should sample with replacement from Model B's cleaned latencies and Model A's cleaned latencies (sample sizes equal to their respective cleaned dataset sizes).
   - Calculate the difference in means for each iteration.
   - The 95% confidence interval is the 2.5th percentile and 97.5th percentile of these 10,000 differences.

4. **Reporting:**
   The script must output a JSON file to `/home/user/report.json` with the following structure (latencies rounded to 2 decimal places):
   ```json
   {
     "model_A_cleaned_count": <int>,
     "model_B_cleaned_count": <int>,
     "mean_diff_observed": <float>,
     "ci_lower": <float>,
     "ci_upper": <float>
   }
   ```
   *Note: `mean_diff_observed` is the difference between the sample means of the cleaned datasets (Model B - Model A).*

Constraints:
- Your entrypoint MUST be `/home/user/pipeline.sh` and it must be executable.
- The pipeline should fully generate `/home/user/report.json` when executed.