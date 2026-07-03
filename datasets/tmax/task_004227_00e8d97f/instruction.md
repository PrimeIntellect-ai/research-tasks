You are assisting a compliance officer in auditing system access records. The company's access control data and organizational structure are stored in an RDF graph file at `/home/user/access_graph.ttl`. 

According to our strict Separation of Duties (SoD) compliance policy, no employee should have access to both the "FinancialSystem" and the "HRSystem" unless they are in the "Executive" department.

Your task is to write a Python script that:
1. Loads the RDF graph from `/home/user/access_graph.ttl` using the `rdflib` library.
2. Uses a SPARQL query to reverse-engineer the graph's structure to identify employees, their departments, and the systems they have access to.
3. Finds all employees who violate the SoD policy (i.e., they have access to *both* the FinancialSystem and HRSystem, but their department is *not* Executive).
4. Exports the results to a CSV file at `/home/user/violations.csv`.

The CSV file must have the following exact headers: `EmployeeID,Name,Department`
The `EmployeeID` should be the URI string of the employee entity.
The rows must be sorted alphabetically by `EmployeeID`.

Example output format for `violations.csv`:
EmployeeID,Name,Department
http://example.org/emp99,John Doe,Engineering

Ensure your Python script is fully self-contained. You can write it to `/home/user/audit.py` and execute it to produce the required CSV.