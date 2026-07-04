You are a data analyst tasked with identifying "super-connectors" within a company's internal collaboration network. You have been provided with two CSV files representing the company's knowledge graph:

1. `/home/user/employees.csv` - Contains employee information.
   Columns: `id`, `name`, `department`
2. `/home/user/collaborations.csv` - Contains undirected edges representing past collaborations between employees.
   Columns: `emp_id_1`, `emp_id_2` (Note: the graph is undirected, so if A collaborated with B, it implies B collaborated with A).

Your objective is to find the most valuable "Cross-Department Bridge" in each department. 

A "Cross-Department Bridge" is formed when an employee (let's call them Y) connects two other employees (X and Z) such that:
1. X and Z are in **strictly different** departments.
2. X and Z have **never** collaborated directly with each other (there is no edge between X and Z in the collaborations file).
3. Both X and Z have collaborated with Y (there are edges X-Y and Y-Z).

The "Bridge Score" for employee Y is the number of **unique pairs** of {X, Z} that satisfy the above conditions. (Note: The pair {X, Z} is considered identical to {Z, X}).

Please write a Python script that calculates the Bridge Score for every employee. Then, find the employee with the highest Bridge Score within each department (simulating an analytical window function like `ROW_NUMBER() OVER (PARTITION BY department ORDER BY bridge_score DESC)`). 

If there is a tie in the Bridge Score within a department, break the tie by choosing the employee with the lowest `id`.

Output the top employee for each department into a CSV file named `/home/user/top_connectors.csv`. 

The output CSV must have exactly the following columns, in this order:
`department,employee_id,name,bridge_score`

The rows in the output CSV should be sorted alphabetically by `department`. Do not include employees with a Bridge Score of 0 in the final output unless all employees in that department have a score of 0 (in which case, pick the lowest ID employee with score 0).