You are acting as a data analyst who needs to process an organizational structure and salary dataset. Since you are operating in a resource-constrained environment without database engines or high-level data processing libraries, you must write a pure C program to process the data.

You have been provided with an input CSV file at `/home/user/data/employees.csv` containing the following columns:
`emp_id,manager_id,salary,department`

Your task is to write a C program (save it as `/home/user/process_csv.c`) that reads this CSV file and calculates the following metrics for each employee:
1. **subordinate_count**: The total number of employees under this employee's hierarchy (direct and indirect reports).
2. **dept_avg_salary**: The average salary of all employees in the same department (formatted to 2 decimal places).
3. **dept_salary_rank**: The employee's salary rank within their department. The highest salary gets rank 1. In case of a tie in salary, the employee with the smaller `emp_id` gets the better (lower) rank number.

The program must output a new CSV file to `/home/user/output/metrics.csv` with the exact header:
`emp_id,subordinate_count,dept_avg_salary,dept_salary_rank`

Requirements:
- The output CSV must be sorted by `emp_id` in ascending order.
- You must use standard C libraries only (`stdio.h`, `stdlib.h`, `string.h`, etc.). No external dependencies are allowed.
- You must compile your C program to `/home/user/process_csv` using `gcc` and then execute it to generate the output file.
- `manager_id` can be the string "NULL" for top-level managers.

Ensure that the output directory exists or create it. Write, compile, and run the program to successfully generate the `metrics.csv` file.