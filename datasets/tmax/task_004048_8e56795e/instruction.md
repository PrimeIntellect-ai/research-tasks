You are a Machine Learning Engineer preparing training data and validating the calibration of a previous model's output. You need to verify if the model's confidence scores roughly match its empirical accuracy using a Bayesian approach.

You have a dataset of model predictions located at `/home/user/predictions.csv`. The file is a comma-separated values file with a header row and the following columns:
1. `id` (integer): Unique identifier
2. `model_score` (float): The predicted probability of success by the model (between 0.0 and 1.0)
3. `is_correct` (integer): Ground truth, where 1 means the model's primary prediction was correct, and 0 means incorrect.

Your task is to write a Rust program (`/home/user/validate.rs`) that does the following without relying on external crates (only standard library is allowed):
1. Reads and parses `/home/user/predictions.csv`.
2. Filters the data to only include rows where the `model_score` is in the interval `[0.70, 0.80)` (i.e., exactly 0.70 up to, but not including, 0.80).
3. Aggregates the filtered tabular data to find:
   - `N`: The total number of predictions in this bin.
   - `K`: The number of correct predictions (`is_correct == 1`) in this bin.
4. Performs a basic Bayesian update to calculate the posterior mean of the true accuracy for this bin. Assume a Uniform prior over the probability of success, which corresponds to a Beta(1, 1) distribution. The posterior distribution will be Beta(1 + K, 1 + N - K), and its expected value (mean) is `(1 + K) / (N + 2)`.
5. Writes the aggregated results to a file at `/home/user/output.txt` in exactly this format:
   `N=<N>,K=<K>,PosteriorMean=<Mean>`
   where `<Mean>` is rounded to exactly 4 decimal places.

For example, if N=3 and K=2, the posterior mean is 3/5 = 0.6. The output should be:
`N=3,K=2,PosteriorMean=0.6000`

Compile your Rust program, run it, and ensure `/home/user/output.txt` is successfully created with the correct values.