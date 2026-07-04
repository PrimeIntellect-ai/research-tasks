You are a database administrator tasked with fixing a reporting bug and building a data export tool. 

We have a SQLite database at `/home/user/company.db` containing an `employees` table with the following schema:
`CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, department_id INTEGER, individual_sales INTEGER);`

Currently, the reporting team uses a flawed SQL query to calculate total sales (an employee's own sales plus the sales of all employees under them in the reporting hierarchy) and their rank within their department. Their query has an implicit cross join that is massively inflating the sales numbers.

Your task is to:
1. Initialize a new Rust project at `/home/user/sales_report`.
2. Add `rusqlite` to the dependencies (use version `"0.29.0"` with the `"bundled"` feature) and `csv` crate (version `"1.3.0"`).
3. Write a Rust program in this project that connects to `/home/user/company.db`.
4. Your Rust program must execute a corrected SQL query that uses:
   - A **Recursive CTE** to correctly traverse the hierarchy (`manager_id` points to the `id` of the employee's manager) and sum the `individual_sales` to calculate `total_sales` for each employee (inclusive of their own sales).
   - A **Window Function** (`DENSE_RANK()`) to calculate the `dept_rank` of each employee based on their `total_sales` descending, partitioned by `department_id`.
5. The Rust program must export the results to `/home/user/report.csv` with the headers exactly as follows:
   `id,name,department_id,total_sales,dept_rank`
6. The CSV output must be sorted by `id` in ascending order.
7. Compile and run your Rust program so that the CSV file is generated.