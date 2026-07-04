You are a data analyst stepping into a project where a previous colleague left behind a broken process. 

In `/home/user/`, there are two CSV files: `employees.csv` and `sales.csv`. 
The previous analyst was trying to generate two reports using an in-memory database, but their SQL query contained an implicit cross join, resulting in massively inflated sales numbers.

Your task is to write a Go program (`/home/user/process.go`) that does the following:
1. Initializes a Go module in `/home/user/` and installs the SQLite3 driver (`github.com/mattn/go-sqlite3`).
2. Reads `employees.csv` and `sales.csv` and loads them into an SQLite database (you can use a file-based DB at `/home/user/data.db`).
3. Constructs and executes a correct SQL query using **Window Functions** to find the top 2 employees by total sales in each department. Sort the results alphabetically by department, and then by total sales descending. Write these results as a JSON array to `/home/user/top_sales.json`. Each JSON object should have the keys: `"department"`, `"name"`, and `"total_sales"`.
4. Constructs and executes a **Recursive CTE** (simulating a graph traversal) to calculate the total sales of the entire organizational hierarchy starting from the CEO (the employee with an empty/null `manager_id`). Write this single total integer value to `/home/user/ceo_sales.txt`.

**Files Details:**
`employees.csv` format: `id,name,manager_id,department`
`sales.csv` format: `employee_id,amount,date`

Write, build, and run your Go program to generate `/home/user/top_sales.json` and `/home/user/ceo_sales.txt`.