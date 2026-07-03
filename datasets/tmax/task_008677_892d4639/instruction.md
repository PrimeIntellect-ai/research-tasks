You are acting as an MLOps engineer. We have recently run several A/B testing experiments on new model versions, and the prediction outcomes (success or failure) have been logged as text artifacts. 

Your task is to write a Bash script that evaluates these models using a simple Bayesian approach and identifies the most promising model.

The experiment logs are located in the directory: `/home/user/artifacts/`.
Each log file is named `<model_name>.log` (e.g., `model_v1.log`).
Inside each log file, each line represents a single prediction trial and contains the string `OUTCOME: 1` for a successful prediction, or `OUTCOME: 0` for a failed prediction.

Because the number of trials varies wildly between models, simple empirical win rates are misleading. You must calculate the expected success rate using a Bayesian Beta-Binomial conjugate model with a uniform prior (a Beta(1, 1) distribution). 

The expected value of the posterior distribution for the success rate is calculated as:
`Expected_Rate = (S + 1) / (N + 2)`
Where:
- `S` is the total number of successes (`OUTCOME: 1`)
- `N` is the total number of trials (`OUTCOME: 1` plus `OUTCOME: 0`)

Write and execute a Bash script at `/home/user/evaluate.sh` that:
1. Iterates through all `.log` files in `/home/user/artifacts/`.
2. Counts the successes and total trials for each model.
3. Calculates the expected success rate (posterior mean) for each model using the formula above.
4. Identifies the model with the highest expected success rate.
5. Writes the best model's name (extracted from the filename, without the `.log` extension) and its expected success rate to `/home/user/best_model.txt`.

The output in `/home/user/best_model.txt` must be strictly in the following format:
`MODEL_NAME,EXPECTED_RATE`

The `EXPECTED_RATE` must be rounded to exactly 4 decimal places (e.g., `0.8333`).

Make sure your script is executable and run it to produce the final `best_model.txt` file. You may use standard Unix utilities like `awk`, `grep`, `bc`, etc., within your Bash script.