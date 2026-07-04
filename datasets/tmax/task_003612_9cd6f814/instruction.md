I am a researcher organizing some experimental datasets, and I need a reproducible Python script to process them, compute a simple Bayesian metric, and log the results for experiment tracking.

I have several CSV files in `/home/user/datasets/`. Each CSV contains the columns `dataset_id`, `trials`, and `successes`. 

Please create a Python script at `/home/user/analyze.py` that does the following:
1. Reads all CSV files in `/home/user/datasets/` and aggregates the data. You need to group by `dataset_id` and sum the `trials` and `successes` across all files for each dataset.
2. For each unique `dataset_id`, calculates the Bayesian posterior mean of the success probability. Assume a Beta-Binomial conjugate model with a uniform-like Beta prior where alpha = 2 and beta = 2. 
   *(Hint: The posterior mean for a Beta(alpha, beta) prior with `s` successes and `n` trials is `(alpha + s) / (alpha + beta + n)`).*
3. Outputs the tracked experiment results to a JSON file at `/home/user/tracking.json`. The JSON must have the following exact structure:
   ```json
   {
     "prior_alpha": 2,
     "prior_beta": 2,
     "results": [
       {"dataset_id": "A", "posterior_mean": 0.1234},
       ...
     ]
   }
   ```
4. The `results` list must be sorted alphabetically by `dataset_id`.
5. The `posterior_mean` values must be rounded to exactly 4 decimal places.

Run the script to produce the `/home/user/tracking.json` file.