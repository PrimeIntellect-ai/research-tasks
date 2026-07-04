You are a data analyst working with an organization's sales data. The company's hierarchy and sales records are exported as flat CSV files, but we need to run hierarchical queries to determine the total sales volume for each employee, which includes their own direct sales PLUS the sales of all employees who report to them (both directly and indirectly).

You have two input files:
1. `/home/user/employees.csv` - Contains `emp_id,emp_name,manager_id`. (The top-level manager has `NULL` or an empty string for `manager_id`).
2. `/home/user/sales.csv` - Contains `emp_id,sale_amount`.

Your task is to write a C++ program `/home/user/aggregate.cpp` that acts as an in-memory aggregation pipeline. The program must:
1. Parse the CSV files and build the organizational hierarchy tree.
2. Recursively aggregate the sales data so that each employee's total includes their own sales and the sales of their entire sub-tree.
3. Validate and export the final aggregated data to a strict output schema. Write the results to `/home/user/total_sales.csv` with exactly two columns: `emp_id,total_sales`. The rows must be sorted by `emp_id` in ascending numerical order.
4. Support a parameterized query via command-line arguments. If the program is executed with `--target-id <ID>`, it should also write the single aggregated integer total for that specific `emp_id` into `/home/user/query_result.txt`.

Once you have written the code, compile it using `g++ -std=c++17 -O2 /home/user/aggregate.cpp -o /home/user/aggregate`.

Finally, execute your program to generate the `/home/user/total_sales.csv` file, and also run a parameterized query for Employee ID `2` like so:
`/home/user/aggregate --target-id 2`

Ensure both `/home/user/total_sales.csv` and `/home/user/query_result.txt` are generated correctly.