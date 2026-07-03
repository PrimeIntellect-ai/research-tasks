You are a data engineer tasked with building a lightweight ETL pipeline using only standard Bash tools (like `awk`, `join`, `sort`, `sed`, `bc`, etc.).

You have been provided with two CSV files in the directory `/home/user/data/`:
1. `/home/user/data/users.csv` - Contains user information. Columns: `id,name,region`
2. `/home/user/data/purchases.csv` - Contains transaction records. Columns: `user_id,amount,date`

Both files contain a header row. 

Your task is to write a Bash script at `/home/user/etl.sh` that performs the following:
1. Joins the two datasets on the user ID (`id` in users.csv and `user_id` in purchases.csv).
2. Calculates the total purchase `amount` for each `region`. You must configure your script to correctly handle floating-point numerical summation (standard to 2 decimal places).
3. Outputs the aggregated results to a new file at `/home/user/summary.csv`.
4. The output file must have a header row: `Region,TotalAmount`.
5. The output rows must be sorted in descending order of the `TotalAmount`.

Ensure your script `/home/user/etl.sh` has executable permissions (`chmod +x`). Do not use Python, Perl, or any non-standard bash tools. The automated testing suite will run `/home/user/etl.sh` and then verify the exact contents of `/home/user/summary.csv`.