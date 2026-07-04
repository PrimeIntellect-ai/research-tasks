You are tasked with optimizing a slow data reporting pipeline and integrating it with a caching layer. 

We have a PostgreSQL database and a Redis instance. Currently, the code to generate the "Top Performers Department Report" is scattered, slow, and fetches too much raw data into memory.

Here is the setup:
1. Two services exist: PostgreSQL (port 5432) and Redis (port 6379). Run `/app/start_services.sh` to start them and seed the `company_db` database.
2. The database `company_db` (user: `admin`, password: `password123`) has two tables:
   - `employees` (emp_id INT, dept_id INT, emp_name VARCHAR)
   - `sales` (sale_id INT, emp_id INT, amount DECIMAL, sale_date DATE)
3. You must write a C++ program at `/home/user/app/report_generator.cpp`. 

Your C++ program must:
- Accept three command-line arguments: `<dept_id>` `<start_date>` `<end_date>` (Dates are in YYYY-MM-DD format).
- Use `libpqxx` to connect to PostgreSQL.
- Construct a parameterized query using CTEs and Window Functions (like `RANK() OVER ...`) to calculate the top 3 employees by total sales amount in the given `dept_id` within the date range (inclusive), AND the total sales of the entire department in that period.
- Connect to Redis (using `hiredis` on localhost:6379) and check if the key `dept_report:<dept_id>:<start_date>:<end_date>` exists. If it does, print its value and exit.
- If it does not exist, execute the optimized SQL query.
- Format the output exactly like this:
  ```
  DEPT: <dept_id> | TOTAL_DEPT_SALES: <total_amount>
  RANK 1: <emp_name> - <emp_total_sales>
  RANK 2: <emp_name> - <emp_total_sales>
  RANK 3: <emp_name> - <emp_total_sales>
  ```
  (Omit ranks if there are fewer than 3 employees with sales. Amounts should be formatted to 2 decimal places).
- Save this exact string to Redis under the key `dept_report:<dept_id>:<start_date>:<end_date>` with a TTL of 60 seconds.
- Print the string to standard output.

Compile your program to `/home/user/app/report_bin` using `g++ -O3 report_generator.cpp -lpqxx -lpq -lhiredis -o report_bin`.

The final binary must be fast and heavily rely on the database for aggregation rather than aggregating in C++. Do not use string concatenation for SQL parameters; use proper parameterized queries (prepared statements in `pqxx`) to prevent SQL injection.