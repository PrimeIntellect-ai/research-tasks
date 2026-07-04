You are an ETL data engineer working on a knowledge graph pipeline. We use RDF graphs to track employee assignments, departments, and project management. Recently, our automated resource allocation transactions have been deadlocking. We traced the issue to "cross-dependencies" between employees.

A cross-dependency occurs between two different employees (Employee A and Employee B) when:
1. Employee A works in a department that manages a project Employee B is assigned to.
2. Employee B works in a department that manages a project Employee A is assigned to.
3. Employee A and Employee B do NOT work in the same department.

Your task is to write a Python script `/home/user/find_cycles.py` that parses a local RDF dataset using the `rdflib` library and executes a SPARQL query to find all such cross-dependent employee pairs. 

The input dataset is located at `/home/user/company_data.ttl`.

Your script must execute the SPARQL query and output the results to `/home/user/cross_dependencies.csv`. 
The CSV must have the following format:
- No header row.
- Two columns separated by a comma, containing the raw URIs of the employees.
- To avoid duplicate pairs (e.g., A,B and B,A), always place the lexicographically smaller URI in the first column, and the larger in the second column.
- Sort the entire CSV alphabetically by the first column, then by the second column.

You will need to install `rdflib` if it is not already installed.