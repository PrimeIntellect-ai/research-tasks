You are a data analyst tasked with processing experiment logs using only standard Linux command-line tools (like `awk`, `join`, `sort`, etc.). 

You have two CSV files:
1. `/home/user/experiments.csv` containing columns: `exp_id,variant,clicks,views`
2. `/home/user/metadata.csv` containing columns: `exp_id,date,category`

Your task is to:
1. Join the two datasets on the `exp_id` column.
2. Filter the joined data to only include experiments where the `category` is exactly `banner`.
3. Aggregate the total `clicks` and total `views` for each `variant` within this filtered dataset.
4. Calculate the Bayesian posterior mean for the click-through rate of each variant. Assume a Beta(1, 1) prior. The formula for the posterior mean is: `(total_clicks + 1) / (total_views + 2)`.
5. Output the results to `/home/user/banner_posteriors.csv`.

The output file `/home/user/banner_posteriors.csv` must:
- Have NO header row.
- Be comma-separated with two columns: `variant,posterior_mean`.
- Have the `posterior_mean` formatted to exactly 4 decimal places (e.g., `0.0459`).
- Be sorted in descending order by the `posterior_mean`.

Do not use Python, R, or any other scripting languages; stick to standard Bash utilities.