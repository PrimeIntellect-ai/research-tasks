You are a Machine Learning Engineer preparing and validating a dataset extracted from server logs before training an anomaly detection model. You need to write a Go program that processes raw log data, engineers new features, and performs statistical validation using bootstrap sampling.

Your task is to create and execute a Go program at `/home/user/analyzer.go` that performs the following steps:

1. **Dataset Preparation & Tokenization**: 
   Read the log file located at `/home/user/data/raw_logs.txt`. 
   Each line in the file has the format: 
   `[TIMESTAMP] [LEVEL] Processed request in <LATENCY>ms with <RETRIES> retries.`
   Parse each line to extract the `<LATENCY>` (as a float64) and `<RETRIES>` (as an int). Ignore any lines that do not strictly match this format or have missing data.

2. **Feature Engineering**:
   For each successfully parsed log line, calculate a new feature called `severity_score` using the formula:
   `severity_score = LATENCY * (RETRIES + 1.5)`

3. **Sampling and Bootstrap Methods**:
   Generate a bootstrap distribution of the mean `severity_score`. 
   To do this, draw 10,000 bootstrap samples (with replacement) from your array of `severity_score`s. Each bootstrap sample must be the same size as your original valid parsed dataset.
   Calculate the mean of each of the 10,000 bootstrap samples.

4. **Confidence Intervals & Hypothesis Testing**:
   Calculate the 95% confidence interval for the mean `severity_score` using the percentile method on your bootstrap means (i.e., the 2.5th and 97.5th percentiles).
   We want to test the null hypothesis ($H_0$) that the true mean severity score is $\le 600$. 
   The alternative hypothesis ($H_1$) is that the true mean $> 600$. 
   Evaluate this by checking if the lower bound of your 95% confidence interval is strictly greater than 600.

5. **Numerical Accuracy & Output**:
   Calculate the exact sample mean of the original `severity_score` array.
   Calculate the mean of your 10,000 bootstrap means.
   
   Output your final results as a JSON file at `/home/user/results.json` with the following exact keys:
   - `"exact_mean"`: The exact sample mean of the original severity scores (float).
   - `"bootstrap_mean"`: The mean of the 10,000 bootstrap means (float).
   - `"ci_lower"`: The 2.5th percentile of the bootstrap means (float).
   - `"ci_upper"`: The 97.5th percentile of the bootstrap means (float).
   - `"reject_null"`: A boolean indicating whether $H_0$ is rejected (true if ci_lower > 600, false otherwise).

Ensure your Go program is completely self-contained, compiles, and successfully writes the JSON file. You may use standard Go libraries.