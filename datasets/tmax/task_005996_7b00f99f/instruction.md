You are a data analyst tasked with analyzing organizational dependencies and project allocations. You have been given two CSV files containing company data. 

Your goal is to write a Python script that converts this tabular data into a graph, and then runs a recursive graph query to extract specific hierarchical insights.

The data files are:
1. `/home/user/employees.csv`
Columns: `emp_id, name, manager_id`
(Note: `manager_id` is the `emp_id` of the person they report to. The CEO has an empty `manager_id`).

2. `/home/user/projects.csv`
Columns: `project_id, project_name, emp_id`
(Shows which employee is working on which project).

Please write a Python script at `/home/user/analyze_org.py` that does the following:
1. Loads the CSV files and constructs an in-memory RDF graph using the `rdflib` library. You should define a namespace `http://example.org/` and use predicates like `reportsTo` and `worksOn`.
2. Takes exactly one command-line argument: a Target Employee ID (e.g., `E002`).
3. Uses a parameterized SPARQL query (using SPARQL 1.1 property paths for recursion) to find all **direct and indirect subordinates** of the Target Employee (i.e., anyone who reports to them, or reports to someone who reports to them, all the way down the chain).
4. Retrieves the names of these subordinates and the names of the projects they are working on. Filter out any subordinates who are not assigned to any projects.
5. Sorts the results alphabetically first by the subordinate's name, and then by the project name.
6. Writes the results to a CSV file at `/home/user/subordinate_projects.csv` with exactly two columns: `employee_name,project_name`. Include a header row.

Before running your script, ensure you install `rdflib` via `pip install --user rdflib pandas`.

To complete the task, execute your script for the employee ID `E002`:
`python3 /home/user/analyze_org.py E002`

Your final output should be strictly in `/home/user/subordinate_projects.csv`.