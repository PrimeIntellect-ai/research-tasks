You are a data engineer working on an ETL pipeline that analyzes organizational structures. We have a dump of employee records extracted from a NoSQL document database, saved locally as a JSON file at `/home/user/employees.json`.

Your task is to write a script (in Python, Node.js, or bash/jq) that performs the following steps:

1. **Document Aggregation & Graph Analytics**: Parse the JSON array. Treat the data as a directed graph where an edge represents a "reports to" relationship (from employee to manager). Calculate the in-degree centrality (number of direct reports) for every employee to find the "bottleneck" manager—the employee with the highest number of direct reports. 
   *Note: If there is a tie for the most direct reports, select the employee with the lowest `emp_id`.*

2. **Recursive / Hierarchical Query**: Once you have identified the bottleneck manager, recursively trace the management chain from the CEO (the employee whose `manager_id` is strictly `null`) down to this bottleneck manager.

3. **Output**: Write the chain of command to a file named `/home/user/bottleneck_chain.txt`. The output must be a single line containing the names of the employees in order, separated by ` -> `. 

For example, if the CEO is "Alice", her direct report is "Bob", and Bob's direct report is the bottleneck manager "Charlie", the file should contain exactly:
`Alice -> Bob -> Charlie`

Ensure the script executes successfully and generates the requested output file.