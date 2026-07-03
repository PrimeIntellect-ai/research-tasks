You are a database administrator tasked with analyzing a corporate knowledge graph stored in an SQLite database. The database contains both hierarchical employee data and a complex network of project dependencies. 

Your goal is to extract specific insights by combining recursive SQL queries with graph analytics.

The database is located at `/home/user/corporate_data.db` and contains two tables:
1. `employees` (emp_id TEXT PRIMARY KEY, name TEXT, manager_id TEXT)
2. `project_dependencies` (project_id TEXT, depends_on_project_id TEXT) - Note: A row `(P1, P2)` means P1 depends on P2.

Please perform the following two tasks using a Python script:

**Task 1: Recursive Hierarchical Query**
Write a recursive CTE (Common Table Expression) SQL query to find all employees who are in the management chain under the employee with `emp_id = 'E001'` (inclusive of 'E001'). 
Write the `emp_id`s of all these individuals to a file named `/home/user/reports_chain.txt`, with one ID per line, sorted in ascending alphabetical order.

**Task 2: Graph Analytics for Bottleneck Detection**
Using the `project_dependencies` table, construct a directed graph where an edge goes from `depends_on_project_id` to `project_id` (representing the flow of requirements/blocking). 
Calculate the PageRank of all nodes in this network (you may use the `networkx` library with its default parameters). Identify the project that is the biggest bottleneck (i.e., the node with the highest PageRank score).
Write the `project_id` of this single biggest bottleneck project to a file named `/home/user/bottleneck_project.txt`.

You can install any necessary Python packages using `pip`.