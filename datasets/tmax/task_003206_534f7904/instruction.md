As a compliance officer, you are auditing our hybrid system to identify unauthorized data access. Our employee records are stored in a relational database (SQLite), but our access control lists (ACLs) and resource hierarchies are managed as a knowledge graph (RDF/Turtle). 

We have a strict compliance rule: **No employee in the "Contractor" department is allowed to have read access to "CustomerData"**, either directly or indirectly through role inheritance.

Your task is to write a Rust application that bridges these two systems, executes the necessary queries, and generates a compliance violation report.

Here are the details of the systems:

1. **Relational Database (SQLite)**:
   - Location: `/home/user/employees.db`
   - Schema:
     - `employee` (id INTEGER PRIMARY KEY, name TEXT, department TEXT)
     - `employee_roles` (emp_id INTEGER, role_uri TEXT)

2. **Access Control Graph (Turtle)**:
   - Location: `/home/user/resources.ttl`
   - Prefixes used in the graph: 
     - `ex:` -> `<http://example.org/>`
     - `role:` -> `<http://example.org/role/>`
   - Edges: 
     - `ex:canRead` maps a role to a resource (e.g., `role:Dev ex:canRead ex:CustomerData .`)
     - `ex:inheritsFrom` maps a role to another role it inherits permissions from (e.g., `role:TempDev ex:inheritsFrom role:Dev .`). *Note: Inheritance can be multi-level/transitive.*

**Requirements:**
1. Create a new Rust project at `/home/user/compliance_auditor`.
2. Write a Rust program that uses the `rusqlite` crate to query the SQLite database for all employees in the `Contractor` department and retrieves their `role_uri`.
3. Use the `oxigraph` crate to load `/home/user/resources.ttl` into an in-memory graph store.
4. Construct and execute a SPARQL query against the graph to determine which of those `role_uri`s have `ex:canRead` access to `<http://example.org/CustomerData>`, taking into account transitive `ex:inheritsFrom` relationships (i.e., if Role A inherits from Role B, and Role B can read CustomerData, Role A can read CustomerData).
5. Cross-reference the results to find violating contractors.
6. Output the results to `/home/user/violation_report.json` in the following exact JSON format:
```json
{
  "violators": [
    {
      "name": "Employee Name",
      "role_uri": "http://example.org/role/ViolatingRole"
    }
  ]
}
```
*If there are multiple violators, sort them alphabetically by name.*

Compile and run your Rust application so that the `violation_report.json` file is successfully generated.