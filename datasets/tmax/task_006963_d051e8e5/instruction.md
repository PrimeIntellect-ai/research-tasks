You are a data engineer building an ETL pipeline using C++ and SQLite. 
You have taken over a project where an existing C++ script (`/home/user/etl/pipeline.cpp`) runs a sequence of SQL commands to process employee data. However, the current pipeline has a major bug in its initial staging query, and it is missing the analytical transformations required by the business.

Your task is to fix the existing bug, implement the missing analytical SQL queries, compile the pipeline, and generate the final report.

Here is the current state of the system:
- A SQLite database is located at `/home/user/data/company.db`. It contains two tables: `employees` (id, name, manager_id, dept_id, salary, hire_date) and `departments` (id, name).
- The source file `/home/user/etl/pipeline.cpp` executes a staging query to combine employees and departments into a table called `stg_emp_dept`. Unfortunately, the query produces heavily inflated and duplicated results because of a flawed table join condition (a classic "cartesian product" issue).

Your objectives:
1. Fix the bug in `/home/user/etl/pipeline.cpp` so that `stg_emp_dept` correctly maps employees to their respective departments.
2. Extend the C++ program to execute a final analytical query that calculates two new columns:
   - `management_level`: Use a Recursive CTE to determine each employee's depth in the management hierarchy. Employees with a NULL `manager_id` are at level 1. Their direct reports are level 2, and so on.
   - `dept_running_total`: Use a Window Function to calculate the running total of `salary` within each department, ordered by `hire_date` ascending.
3. The final query should select the following columns in order: `emp_id, emp_name, dept_name, management_level, salary, dept_running_total`. Order the final result by `dept_name` ascending, then `hire_date` ascending.
4. Modify the C++ program to write the results of this final query to a CSV file at `/home/user/etl/final_report.csv`. The CSV should include a header row with the exact column names specified in step 3.

Compilation and execution:
- You must compile the C++ program. You can use standard tools available on Linux (e.g., `g++ -std=c++17 pipeline.cpp -lsqlite3 -o pipeline`).
- Run the compiled binary to generate `/home/user/etl/final_report.csv`.

Note: You may need to install the SQLite C++ development headers if they are not present on the system (`libsqlite3-dev`). Make sure all files are created in the exact locations requested.