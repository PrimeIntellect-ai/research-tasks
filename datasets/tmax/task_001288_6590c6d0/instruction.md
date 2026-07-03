You are an MLOps engineer responsible for tracking experiment artifacts and evaluating model performance. A recent batch inference job has completed, and the raw logs have been dumped to a CSV file. 

Your task is to validate the model outputs, parse the inference times, and use bootstrap sampling to estimate the confidence interval of our latency metrics to ensure we meet our Service Level Agreements (SLA).

The data is located at `/home/user/experiment_data.csv`. 
The CSV has the following columns:
`req_id,predicted_class,confidence_score,inference_time_ms`

Write a Python script (you can name it whatever you want, e.g., `analyze.py`) that performs the following steps:

1. **Model Output Validation:**
   Filter the dataset to keep ONLY rows that meet all the following strict criteria:
   - `predicted_class` must be exactly 3 uppercase letters (e.g., "CAT", "DOG").
   - `confidence_score` must be a valid floating-point number between 0.0 and 1.0 (inclusive). Missing or unparseable values should be discarded.
   - `inference_time_ms` must be a valid positive float.

2. **Inference Performance Benchmarking & Bootstrapping:**
   Extract the `inference_time_ms` for all valid rows. We want to estimate the 95% Confidence Interval for the **90th percentile (P90)** inference time.
   - Import `numpy` and set the random seed exactly to `42` (`numpy.random.seed(42)`).
   - Perform bootstrap resampling: Create exactly `10,000` bootstrap samples. Each bootstrap sample must be drawn with replacement from your valid `inference_time_ms` array and must be the exact same size as the valid dataset.
   - For each bootstrap sample, compute the 90th percentile (`numpy.percentile(sample, 90)`).
   - Finally, compute the 95% Confidence Interval of these 10,000 P90 values by taking the 2.5th and 97.5th percentiles of the bootstrap distribution.

3. **Reporting:**
   Create a JSON file at `/home/user/report.json` containing the exact following keys:
   - `"valid_count"`: The integer number of rows that passed validation.
   - `"p90_ci_lower"`: The lower bound of the 95% CI (float, rounded to 2 decimal places).
   - `"p90_ci_upper"`: The upper bound of the 95% CI (float, rounded to 2 decimal places).

Ensure all code executes successfully and `/home/user/report.json` is generated with the correct format and values.