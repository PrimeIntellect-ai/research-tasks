You are a data scientist tasked with building the final inference script for a distributed text classification and data cleaning pipeline. The system consists of multiple microservices that need to be properly configured and glued together, and you must write a highly precise Python script to perform Bayesian inference and outlier detection.

System Components:
1. **Redis Cache**: Running locally on port 6379. It stores Bayesian priors and token log-likelihoods for our model (Class A vs Class B).
2. **Tokenizer API (Flask)**: Located in `/app/tokenizer/api.py`. It provides a `/tokenize` endpoint but currently fails because it is misconfigured.

Your objectives:

**Phase 1: Service Configuration & Startup**
1. The Tokenizer API requires an environment variable `REDIS_HOST` to be set to `127.0.0.1`. You must start the Redis server (if not already running) and the Tokenizer API (on port 5000).
2. The API expects a configuration file at `/app/tokenizer/config.json` with the exact contents: `{"max_length": 50, "strip_punctuation": true}`. Create this file before starting the API.

**Phase 2: The Inference Script**
Write a Python script at `/home/user/infer.py` that takes exactly one command-line argument (a raw text string). The script must perform the following deterministic steps:

1. **Tokenization**: Send a POST request to `http://127.0.0.1:5000/tokenize` with JSON payload `{"text": "<input_string>"}`. Extract the `tokens` array from the response. If the array is empty, print `0.0000` and exit.
2. **Missing Value & Outlier Handling (Confidence Intervals)**: 
   Calculate the mean and sample standard deviation (ddof=1) of the lengths of the tokens. 
   Compute the 95% confidence interval for the mean token length using the Z-value 1.96: 
   `Margin of Error = 1.96 * (std_dev / sqrt(N))`
   If the standard deviation cannot be calculated (N=1), assume Margin of Error = 0.
   If the *upper bound* of this confidence interval is strictly greater than `12.0`, consider the text an outlier, print `-1.0000`, and exit.
3. **Bayesian Inference**:
   Connect to the local Redis instance (db=0). 
   Retrieve the prior log-probability for Class A at the key `prior_A`. (Fallback to `-0.5` if missing).
   For each token in the tokenized list:
     - Query Redis for the token's log-likelihood given Class A at key `token_A:<token>`.
     - If the token is missing in Redis (missing value), use a default log-likelihood of `-5.0`.
     - Sum the prior and all token log-likelihoods to get the unnormalized log-posterior for Class A.
4. **Output**: Print the final unnormalized log-posterior for Class A rounded to exactly 4 decimal places (e.g., `-15.2300`). Do not print anything else.

Ensure your script is executable (`chmod +x /home/user/infer.py`) and has `#!/usr/bin/env python3` at the top. The automated test will invoke your script hundreds of times with random strings and compare its exact output to a reference implementation.