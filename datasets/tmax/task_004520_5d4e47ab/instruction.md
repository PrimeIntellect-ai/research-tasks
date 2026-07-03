You are acting as a data analyst. We have a data processing pipeline written in Go that reads two CSV files (`/home/user/users.csv` and `/home/user/transactions.csv`) and generates an aggregated JSON report. 

However, the script (`/home/user/process.go`) has a major bug. The original author tried to manually implement a join and aggregation, but they made a logic error equivalent to an "implicit cross join". As a result, the script assigns every single transaction to every single user, leading to massively inflated `total_spent` values. Furthermore, the script is supposed to calculate the maximum single transaction amount for each user (similar to a window function `MAX(amount) OVER (PARTITION BY user_id)`), but this is currently broken.

Your task is to:
1. Analyze the CSV files and reverse-engineer the intended data model.
2. Fix the bug in `/home/user/process.go` so that it correctly maps transactions to their respective users.
3. Implement the missing logic in Go to calculate the correct `total_spent` (sum of amounts) and `max_transaction` (the highest single transaction amount) for each user. If a user has no transactions, these values should be `0.00`.
4. Run your fixed Go script. It must output the corrected data to `/home/user/output.json`.

The final `/home/user/output.json` must contain a JSON array of objects with the following exact keys and types:
- `user_id` (string)
- `name` (string)
- `total_spent` (float64, rounded to 2 decimal places)
- `max_transaction` (float64, rounded to 2 decimal places)

The output JSON array should be sorted by `user_id` in ascending order.