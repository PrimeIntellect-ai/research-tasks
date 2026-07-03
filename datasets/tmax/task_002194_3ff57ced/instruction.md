You are a data analyst who needs to process some organizational data. You have been provided with two CSV files located in `/home/user/`:
1. `/home/user/employees.csv` - Contains the employee management hierarchy.
   Columns: `emp_id`, `name`, `manager_id`
   (Note: The CEO has an empty `manager_id`)

2. `/home/user/projects.csv` - Contains project assignments, including hours worked and cost per project for each employee.
   Columns: `emp_id`, `project_name`, `hours`, `cost`

Your task is to write and execute a C++ program that reads these CSV files and computes a "rolled-up" summary of hours and costs for every employee. An employee's rolled-up hours and costs are defined as the sum of their own direct project hours and costs, PLUS the rolled-up hours and costs of all their direct and indirect reports (i.e., the entire management sub-tree under them).

Requirements:
1. Write a C++ program in `/home/user/process_data.cpp`.
2. The program must read the two CSV files.
3. It must compute the hierarchical aggregation (recursive rollup) of `hours` and `cost`.
4. It must output the results to a new CSV file at `/home/user/summary.csv`.
5. The output CSV must have the following header exactly: `emp_id,total_hours,total_cost`.
6. The rows in `summary.csv` must be sorted by `emp_id` in ascending numerical order.
7. Use standard C++17 (or C++11/14). You may only use standard libraries (no third-party CSV parsers or external libraries).
8. Compile and run your program so that `/home/user/summary.csv` is generated successfully.

Please ensure the output formatting is strict, as it will be evaluated programmatically. Do not include spaces after commas in the output CSV.