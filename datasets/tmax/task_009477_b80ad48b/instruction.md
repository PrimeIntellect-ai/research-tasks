You are acting as a compliance officer auditing an organization's access logs to find policy violations. 

The company's organizational structure, department hierarchy, and system access logs are stored in an RDF graph file at `/home/user/org_graph.ttl`. 

According to company compliance policies, only employees in the "IT" department (or any of its sub-departments) and the "Security" department (or any of its sub-departments) are allowed to access "System_Omega". 

Your task is to write a Python script at `/home/user/audit.py` that:
1. Uses the `rdflib` library to load `/home/user/org_graph.ttl`.
2. Executes SPARQL queries to extract and aggregate all employees who have accessed `System_Omega` but are **not** authorized (i.e., they do not belong to IT, Security, or any of their sub-departments).
3. Evaluates a hypothetical migration of this access data to a relational SQL database. You must formulate an index strategy for an `access_logs` table (columns: `log_id`, `emp_id`, `system_name`, `access_time`) to strictly optimize queries that filter by `system_name` and order the results by `access_time` descending.
4. Exports the final aggregated data and your index strategy into a precise JSON file at `/home/user/audit_report.json`.

The output JSON must strictly match the following format:
```json
{
  "unauthorized_accesses": [
    {
      "employee_name": "John Doe",
      "department_name": "Sales"
    }
  ],
  "index_strategy": "CREATE INDEX idx_name ON access_logs (column1, column2 DESC);"
}
```
*Notes:*
- The `unauthorized_accesses` list should be sorted alphabetically by `employee_name`.
- The `index_strategy` must be a valid PostgreSQL `CREATE INDEX` statement named `idx_system_time`.
- In the RDF graph, relationships use standard custom prefixes which you will see when inspecting the file.
- You can install `rdflib` using `pip install rdflib` if it is not already installed.