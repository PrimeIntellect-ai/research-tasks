You are acting as an MLOps engineer analyzing unstructured artifact logs from a recent model training sweep. 

You have a raw log file located at `/home/user/raw_experiments.txt`. Each line in this file represents a training run and contains semi-structured text with a model ID, a run status, and a comma-separated list of hyperparameter tokens.

Your task:
1. Build a simple Python script to process this file (ETL and tokenization). Parse each line to find all runs that used the hyperparameter token `dropout_0.5`.
2. Count the number of "Success" and "Failure" outcomes specifically for runs containing the `dropout_0.5` token.
3. Perform a Bayesian update to estimate the true success rate of the `dropout_0.5` hyperparameter. Use a Beta-Binomial conjugate model with a uniform prior of Beta(1, 1).
4. Calculate the posterior Alpha, posterior Beta, and the expected value (mean) of the posterior distribution.
5. You may need to install standard mathematical packages if you prefer, but standard library Python is sufficient.
6. Write the final results to a JSON file at `/home/user/artifact_stats.json` with the following exact keys:
   - `prior_alpha` (integer)
   - `prior_beta` (integer)
   - `posterior_alpha` (integer)
   - `posterior_beta` (integer)
   - `posterior_mean` (float)

Do not include any other keys in the JSON file. Ensure your script is reproducible and operates solely on the provided text log.