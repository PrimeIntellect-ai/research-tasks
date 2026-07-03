You are a data scientist tasked with cleaning inference logs and benchmarking the performance of two machine learning models (Model A and Model B). 

You have been provided with two raw log files containing mixed log levels and text:
- `/home/user/raw_logs_A.txt`
- `/home/user/raw_logs_B.txt`

Your task is to build a small, reproducible ETL and analysis pipeline that does the following:

1. **ETL Process**: Parse both log files. Extract the inference latency values (in milliseconds) from lines that contain the exact string `"Inference time:"`. The line format is typically `[TIMESTAMP] INFO - Inference time: <value> ms`. Ignore any lines that do not match this pattern (e.g., errors, timeouts, or malformed lines).
2. **Benchmarking & Statistical Testing**: 
   - Calculate the sample mean latency for Model A and Model B.
   - Perform a two-sided Welch's t-test (assuming unequal variances) to test the null hypothesis that the two models have the same mean latency.
   - Calculate the 95% confidence interval for the difference in means (`Mean A - Mean B`).
3. **Reporting**: Output your final results to a JSON file located at `/home/user/benchmark_results.json`. The JSON file must have exactly the following keys, with values rounded to 4 decimal places:
   - `"mean_A"`: Mean latency of Model A
   - `"mean_B"`: Mean latency of Model B
   - `"p_value"`: The p-value from the Welch's t-test
   - `"ci_lower"`: The lower bound of the 95% confidence interval for (`Mean A - Mean B`)
   - `"ci_upper"`: The upper bound of the 95% confidence interval for (`Mean A - Mean B`)

Write a script in the language of your choice (Python is recommended, utilizing `scipy.stats`) to process the data, perform the statistical tests, and generate the JSON report. Execute your script to produce the final file.