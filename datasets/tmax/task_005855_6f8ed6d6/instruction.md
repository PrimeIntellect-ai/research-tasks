You are acting as a data analyst. I have a Python script located at `/home/user/process_sales.py` that processes three CSV files (`customers.csv`, `orders.csv`, and `items.csv`) by loading them into an SQLite database and running a query to calculate the total amount spent by each customer. 

However, the current script is producing wildly incorrect, inflated totals because the SQL query contains a bug (an implicit cross join). Additionally, the script does not format or validate the output correctly.

Your task is to:
1. Fix the SQL query inside `/home/user/process_sales.py` so that it correctly joins the tables and calculates the true `total_spent` for each customer.
2. Modify the script so that it outputs the final results to `/home/user/summary.json`. 
3. The output must be a JSON array of objects, strictly adhering to the JSON schema provided in `/home/user/schema.json`. The keys must be `"customer_name"` and `"total_spent"` (represented as a float rounded to 2 decimal places).
4. Run your fixed script to generate the correct `/home/user/summary.json`.

Do not change the names or locations of the input files. Ensure your final JSON file exactly matches the calculated totals without any duplicate counting caused by the previous cross join.