You are a data analyst tasked with processing product data and validating a matching model.

You have a local, vendored copy of the `fuzzywuzzy` package (version 0.18.0) located at `/app/fuzzywuzzy`. However, this package has a deliberate perturbation: a bug was recently introduced into the `fuzz.ratio` function inside `fuzzywuzzy/fuzz.py` that causes it to always return `0`. 

Your tasks are:
1. Fix the bug in `/app/fuzzywuzzy/fuzzywuzzy/fuzz.py` so that `ratio` works correctly again, and install the package locally in editable mode or standard mode into your environment.
2. Build an ETL pipeline to process two datasets located at `/home/user/data_A.csv` and `/home/user/data_B.csv`. Each contains an `item_name` column.
3. Compute the `fuzz.ratio` similarity score for all pairwise combinations of `item_name` between `data_A` and `data_B`.
4. Validate a model's output using `/home/user/model_predictions.csv`, which contains columns `item_A`, `item_B`, and `predicted_match` (1 for a predicted match, 0 otherwise). Extract the computed `fuzz.ratio` score for every pair where `predicted_match == 1`.
5. Apply a bootstrap method to construct a 95% confidence interval for the mean similarity score of these predicted matches.
    - Use exactly `10,000` resamples.
    - Set the random seed to `42` (e.g., `numpy.random.seed(42)`).
    - Use the percentile method (2.5th and 97.5th percentiles) on the resampled means.
6. Create a text file at `/home/user/ci_output.txt` containing exactly the lower and upper bounds of your confidence interval, separated by a comma (e.g., `65.43,72.19`).

Ensure your final numbers are accurate. The automated test will parse your output file and compare your interval against the mathematically correct reference value.