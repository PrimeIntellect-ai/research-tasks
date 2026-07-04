You are acting as a compliance officer auditing an interconnected system of user permissions and resource access logs. The organization's access logs and employee directory are stored in an RDF graph database located at `/home/user/access_graph.ttl`.

Your task is to write a Python script `/home/user/audit.py` that queries this RDF graph to identify and summarize unauthorized after-hours access to highly sensitive resources.

Requirements:
1. You must use the `rdflib` library in Python to parse the Turtle file and execute a SPARQL query. You may need to install it.
2. The script must be executable from the command line and accept the following arguments via `argparse`:
   - `--dept`: The department name to filter by (e.g., "Finance")
   - `--resource`: The specific resource name to filter by (e.g., "Resource_ProjectX")
   - `--min-hour`: The minimum access hour, inclusive (integer)
   - `--max-hour`: The maximum access hour, inclusive (integer)
   - `--output`: The path where the final JSON report will be saved.
3. The script must construct a parameterized SPARQL query. You must pass the department, resource, min-hour, and max-hour as bound variables to the SPARQL execution context (e.g., using `initBindings` in `rdflib`), rather than string-concatenating them directly into the query body.
4. The SPARQL query should find all `AccessEvent` instances where:
   - The event's `accessedBy` links to an `Employee` who has the specified `department`.
   - The event's `accessedResource` matches the provided resource URI (in the `http://example.org/` namespace).
   - The event's `accessHour` is between `--min-hour` and `--max-hour` (inclusive).
5. Extract the `name` of the employee from the query results.
6. The Python script must aggregate the results and output a JSON file containing a dictionary where the keys are the employee names (strings) and the values are the total count of their unauthorized access events (integers).

Graph Schema details (Namespace `http://example.org/`, prefix `ex:`):
- Employees are of type `ex:Employee` and have `ex:name` (string) and `ex:department` (string).
- Access events are of type `ex:AccessEvent`.
- Events link to employees via `ex:accessedBy`.
- Events link to resources via `ex:accessedResource` (the resource itself is an IRI, e.g., `ex:Resource_ProjectX`).
- Events have an `ex:accessHour` (integer).

Once your script is ready, execute it with the following parameters to generate the final report:
`python3 /home/user/audit.py --dept Finance --resource Resource_ProjectX --min-hour 18 --max-hour 23 --output /home/user/audit_report.json`