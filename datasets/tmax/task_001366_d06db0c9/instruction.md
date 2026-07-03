You are acting as a data analyst. I have two CSV files representing our company's employee hierarchy and the project budgets assigned to them. 

Files:
1. `/home/user/employees.csv` - Contains `emp_id`, `emp_name`, and `manager_id`. (The CEO has an empty `manager_id`).
2. `/home/user/projects.csv` - Contains `proj_id`, `emp_id`, and `budget`. 

A previous analyst wrote a script to calculate the total budget responsible by each employee, but it produced wildly inflated numbers due to an implicit cross join and failed to account for the organizational hierarchy.

Your task is to write a script (in bash, Python, SQLite, or any language of your choice) to calculate the **rolled-up total budget** for every employee. An employee's rolled-up total budget is the sum of the budgets of all projects directly assigned to them, **plus** the rolled-up budgets of all employees who report to them (directly or indirectly).

Requirements:
- Calculate the rolled-up budget for every employee present in `employees.csv`.
- If an employee has no projects and no subordinates with projects, their total budget should be 0.
- Save the result to `/home/user/rollup.json`.
- The output must be a strict JSON array of objects, sorted by `emp_id` in ascending order.
- Each object must have exactly two keys: `"emp_id"` (integer) and `"total_budget"` (integer).

Example output structure:
```json
[
  {
    "emp_id": 10,
    "total_budget": 18000
  },
  {
    "emp_id": 20,
    "total_budget": 14000
  }
]
```

Please run your script and ensure `/home/user/rollup.json` is generated with the correct data.