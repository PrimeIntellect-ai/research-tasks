You are a data analyst tasked with building an automated ETL and scoring pipeline using Bash. 

You have been provided with three CSV files located in `/home/user/data/`:
1. `/home/user/data/users.csv` - Contains user demographics. (Columns: `user_id,age_group,region`)
2. `/home/user/data/orders.csv` - Contains order history. (Columns: `order_id,user_id,order_amount,days_active`)
3. `/home/user/data/returns.csv` - Contains return history. (Columns: `order_id,return_amount`)

Your objective is to write a Bash script at `/home/user/run_pipeline.sh` that reads these files, joins the data, calculates specific features, performs a simple predictive regression and classification, and outputs a final CSV.

The script must produce a file at `/home/user/user_features.csv` with the following requirements:
- **Header:** `user_id,total_net_spend,max_days_active,predicted_LTV,segment`
- **Data Rows:** One row per `user_id` found in `users.csv`, sorted numerically by `user_id` in ascending order.
- **Formulas:**
  - `total_net_spend`: For a given user, the sum of all their `order_amount` minus the sum of all their `return_amount`. (If an order has no return, subtracted amount is 0. If a user has no orders, net spend is 0).
  - `max_days_active`: The maximum `days_active` value across all orders for that user. (If a user has no orders, default to 1).
  - `predicted_LTV` (Predictive Regression): Calculated as `total_net_spend + (total_net_spend / max_days_active) * 30`. This value must be rounded to exactly two decimal places.
  - `segment` (Classification): 
    - "VIP" if `predicted_LTV` >= 500.00
    - "Standard" if 100.00 <= `predicted_LTV` < 500.00
    - "Churn_Risk" if `predicted_LTV` < 100.00

**Constraints:**
- Your Bash script (`/home/user/run_pipeline.sh`) must be executable.
- You may use standard Unix tools (awk, sed, join, sort) or embed Python/Perl/Ruby code within your Bash script to accomplish the task.
- Ensure the output file is formatted as a strict comma-separated values file without spaces around the commas.