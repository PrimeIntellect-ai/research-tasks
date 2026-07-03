You are a database administrator tasked with optimizing and restructuring how organizational hierarchy data is processed. You have received an RDF file containing the company's department hierarchy and employee assignments, but your downstream systems require this data to be queried using relational methods.

Your objective is to extract the graph data using SPARQL, project it into a relational database, perform recursive queries to flatten the hierarchy, and aggregate the results.

Here are the specific requirements:
1. A Turtle (RDF) file will be located at `/home/user/data.ttl`. It contains an organizational graph.
2. You must write a Python script that uses SPARQL (e.g., via the `rdflib` library, which you may need to install) to parse `/home/user/data.ttl` and extract:
   - All departments and their parent departments.
   - All employees and the department they directly work in.
3. You MUST project and materialize this raw graph data into a new SQLite database located at `/home/user/org.db`. 
   Create two tables with the exact following schemas:
   - `departments (dept_name TEXT, parent_name TEXT)`
   - `employees (emp_name TEXT, dept_name TEXT)`
   Populate these tables using the literal names (strings) of the entities extracted from the RDF. The root of the company is "Corporation". Note that "Corporation" itself does not have a parent department (you can leave its parent as NULL or an empty string, or omit it if your logic prefers, but represent the rest accurately).
4. After materializing the database, you MUST write a SQL query containing a **recursive CTE** (Common Table Expression) to be executed against `/home/user/org.db`. 
   This recursive query should traverse the hierarchy to find the "top-level" department for each employee. A top-level department is defined as any department whose immediate parent is "Corporation".
5. Perform cross-query aggregation in your SQL or Python code to calculate the total number of employees under each top-level department (including employees in nested sub-departments).
6. Save the final aggregated counts as a JSON file at `/home/user/dept_summary.json`. The JSON should be a single dictionary mapping the top-level department name to its integer employee count.

Example expected format for `/home/user/dept_summary.json`:
```json
{
  "Engineering": 5,
  "Sales": 2
}
```

Ensure your Python script runs end-to-end, performs the SPARQL projection, executes the recursive SQLite CTE, and generates the final JSON file.