You are acting as an automated assistant for a compliance officer auditing an enterprise system's access control graph. 

The company's IAM (Identity and Access Management) and organizational data has been exported as a knowledge graph to a JSON file located at `/home/user/audit_graph.json`. 

The graph contains two top-level keys: `nodes` and `edges`.
Nodes have: `id`, `type` (Employee, Department, Role, Database), and type-specific properties (e.g., `name` for all, `contains_pii` (boolean) for Database).
Edges have: `source` (node id), `target` (node id), and `relationship` (WORKS_IN, HAS_ROLE, CAN_ACCESS).

A major compliance violation occurs when an `Employee` has access to a `Database` where `contains_pii` is `true`, BUT that employee does NOT work in the "HR" or "Compliance" departments. 
Access is determined by the path: Employee -> HAS_ROLE -> Role -> CAN_ACCESS -> Database.
Department membership is determined by: Employee -> WORKS_IN -> Department.

Your task:
1. Write a Python script at `/home/user/audit_script.py` to parse this graph without using external graph databases (you may use standard libraries).
2. Find all employees who are in violation of the PII access rule.
3. For each violating employee, calculate the total number of DISTINCT PII databases they can access.
4. Sort the results descending by the number of unauthorized databases, then ascending alphabetically by the employee's name.
5. Limit the output to the top 3 offenders (pagination/limiting).
6. Write the results to a CSV file at `/home/user/compliance_report.csv` with exactly the following header: `employee_id,employee_name,unauthorized_db_count`.

You must create `/home/user/audit_script.py` and execute it to generate `/home/user/compliance_report.csv`. Ensure you handle the file paths exactly as specified.