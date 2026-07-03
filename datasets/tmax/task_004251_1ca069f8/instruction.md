You are a data engineer building ETL pipelines. Your team uses a vendored bash package to enforce data schemas, and you need to build a statistical filter to detect anomalous "bot" traffic using a Naive Bayes classifier.

Recently, the vendored tool `bash-datakit` (located at `/app/vendored/bash-datakit`) has been misconfigured. Similar to a visualization script producing blank plots, this script is currently dropping valid data or producing blank outputs due to a bug in its validation logic. 

Your objectives are:

1. **Fix the Vendored Package**:
   Inspect and fix `/app/vendored/bash-datakit/validate_csv.sh`. It is supposed to enforce a strict 3-column CSV schema (`user_id,action,geo`) and print valid rows to stdout. Currently, it produces empty lines instead of preserving valid rows.

2. **Implement a Bayesian Filter**:
   Write a bash script at `/home/user/detector.sh` with the following signature:
   `./detector.sh <input_csv> <output_csv>`

   Your script must:
   - First, run the input CSV through the fixed `validate_csv.sh` to enforce the schema and remove malformed rows.
   - Next, use the training data provided at `/app/data/train.csv` to train a **Naive Bayes classifier**. The training data has 4 columns: `user_id,action,geo,is_bot` (where `is_bot=1` means bot, `is_bot=0` means human).
   - Calculate the prior probabilities of `is_bot` and the conditional probabilities of the features `action` and `geo` given `is_bot`. **You must apply Laplace smoothing (add 1 to all feature counts and add the number of distinct feature values to the denominator) to avoid zero probabilities.** 
   - Apply this probabilistic model to evaluate each row of the validated input data. If the posterior probability of being a bot is strictly greater than the probability of being a human:
     `P(is_bot=1 | action, geo) > P(is_bot=0 | action, geo)`
     you must reject (filter out) the row.
   - Write the preserved (human) rows to `<output_csv>`. Ensure the CSV header (`user_id,action,geo`) is included at the top of the output file.

You are expected to use standard Unix tools (bash, awk, grep, etc.) to accomplish this. Do not use Python, R, or other higher-level languages for the implementation of the model or the pipeline.

The automated verifier will test your script against two directories:
- `/app/data/clean/`: Contains CSVs with only normal human records. Your script must preserve 100% of these valid records.
- `/app/data/evil/`: Contains CSVs with bot records. Your script must reject 100% of these records.