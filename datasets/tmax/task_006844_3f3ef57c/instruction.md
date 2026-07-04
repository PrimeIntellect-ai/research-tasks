You are a data analyst tasked with processing internal company communication records. You have been provided with three CSV files in `/home/user/data/`:
1. `departments.csv` (`dept_id`, `dept_name`)
2. `employees.csv` (`emp_id`, `name`, `dept_id`)
3. `communications.csv` (`msg_id`, `sender_id`, `receiver_id`, `timestamp`)

Your goal is to build a SQLite database, design an indexing strategy, aggregate the data, and perform a graph centrality analysis using Python.

Perform the following steps:
1. Load the three CSV files into a SQLite database located at `/home/user/company.db`. You must enforce appropriate foreign key constraints in your schema.
2. Design and create indexes on the tables to optimize a query that joins `communications` to `employees` (to find sender and receiver departments). You must create at least two secondary indexes.
3. Write a SQL query (executed via Python) to aggregate the total number of messages sent *between* different departments. Exclude any messages where the sender and receiver belong to the same department.
4. Using Python and a graph library (like `networkx`), build a directed graph from this aggregated data. Nodes represent department names, and directed edges represent the flow of messages (edge weight = total messages sent from the sender's department to the receiver's department).
5. Calculate the weighted in-degree for each department (the sum of the weights of all incoming edges).
6. Output a final JSON report at `/home/user/results.json` with the following structure:
```json
{
  "total_inter_dept_messages": <int, total count of all messages between different departments>,
  "top_dept_in_degree": "<string, name of the department with the highest weighted in-degree>",
  "indexes_created": ["<string, index1_name>", "<string, index2_name>"]
}
```

Constraints:
- Do not include intra-department messages in the graph or the `total_inter_dept_messages` count.
- You must use Python to drive the SQLite ingestion, querying, and graph analysis.
- Ensure your indexes are actually created in the `company.db` database.