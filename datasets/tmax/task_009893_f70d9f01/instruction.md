You are an operations data scientist analyzing system logs to detect potentially compromised accounts. You have two datasets that you need to clean, aggregate, and merge using only standard Linux command-line tools (Bash, awk, sed, join, etc. - no Python or R).

The files are located in `/home/user/`:
1. `/home/user/activity.log` - A space-separated log file with the format: `timestamp user_id event_type event_value`
   - `event_type` can be `LOGIN` (where `event_value` is `SUCCESS` or `FAIL`) or `PURCHASE` (where `event_value` is a numerical amount in USD).
2. `/home/user/priors.csv` - A comma-separated file with the format `user_id,prior_prob`, containing the baseline prior probability of an account being compromised (between 0.01 and 0.99).

Your task is to compute a posterior risk score for each user present in `priors.csv` based on their activity in `activity.log`. 

For each `user_id` in `priors.csv`:
1. Calculate `N_logins`: The total number of `LOGIN` events for the user.
2. Calculate `N_fails`: The total number of `LOGIN` events where the value is `FAIL`.
3. Calculate `Total_purchase`: The sum of all `PURCHASE` values for the user. (If a user has no purchases, this is 0).
4. Extract `Prior`: The prior probability from `priors.csv`.

Next, compute the Posterior Risk using a simplified Bayesian update:
- Calculate the Likelihood Ratio (`LR`): `LR = ((N_fails + 1) / (N_logins + 2)) * ((Total_purchase + 10) / 100)`
- Calculate the Prior Odds: `Odds = Prior / (1 - Prior)`
- Calculate the New Odds: `New_Odds = Odds * LR`
- Calculate the Posterior Probability: `Posterior = New_Odds / (1 + New_Odds)`

Create a file named `/home/user/risk_scores.csv` containing the final results.
The format must be exactly: `user_id,posterior`
Sort the file alphabetically by `user_id`.
Format the `posterior` value to exactly 4 decimal places (e.g., `0.1230`). If a user from `priors.csv` has no activity in the log, they should still be included in the output (their `N_logins`, `N_fails`, and `Total_purchase` will be 0).