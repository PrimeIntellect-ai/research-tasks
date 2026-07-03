You are a data engineer tasked with building a lightweight, highly reproducible ETL pipeline using only standard Linux shell tools (Bash, awk, sort, join, etc.).

You have been given two comma-separated data files without headers:
1. `/home/user/logins.csv` contains `user_id`, `login_count`, and `days_inactive`.
2. `/home/user/subs.csv` contains `user_id` and `plan_type`.

Your objective is to write a bash script at `/home/user/etl.sh` that performs the following steps and saves the final output to `/home/user/processed.csv`:

1. **Schema Enforcement**: Filter `/home/user/logins.csv` to only include rows where both `login_count` and `days_inactive` are strictly non-negative integers (contain only digits). Discard any malformed rows.
2. **Multi-source Joining**: Join the valid logins data with `/home/user/subs.csv` based on `user_id` (the first column in both files). Only include users present in both files (inner join).
3. **Classification Rule**: Apply a simple heuristic classification to predict churn risk. If a user's `login_count` is less than `5`, classify them as `HighRisk`. Otherwise, classify them as `LowRisk`.
4. **Formatting**: The final output file `/home/user/processed.csv` must be comma-separated, with no headers, sorted alphabetically by `user_id`, and strictly match the following column order:
   `user_id,plan_type,login_count,churn_risk`

Ensure your script `/home/user/etl.sh` is executable and deterministically overwrites `/home/user/processed.csv` with the correct results each time it is run (pipeline reproducibility). Once you have written the script, run it to generate the output file.