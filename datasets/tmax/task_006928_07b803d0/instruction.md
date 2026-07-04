You are a Database Administrator working on integrating a legacy SQLite database with a new RDF-based knowledge graph. The current process is slow and manual. Your task is to write a Python script that extracts data using a complex SQL query, joins it with graph data via SPARQL, validates the output against a JSON schema, and saves the final results.

Here is the setup:
1. **SQLite Database (`/home/user/company.db`)**: 
   Contains three tables:
   - `departments` (id INTEGER, name TEXT)
   - `employees` (id INTEGER, name TEXT, manager_id INTEGER, dept_id INTEGER)
   - `projects` (id INTEGER, name TEXT, lead_id INTEGER)
   
2. **RDF Knowledge Graph (`/home/user/knowledge.ttl`)**:
   A Turtle file containing project metadata. It uses the prefix `ex: <http://example.org/>`.
   Projects are represented as nodes, and have properties `ex:projectName` (literal matching the database `name`) and `ex:riskLevel` (literal).

3. **JSON Schema (`/home/user/schema.json`)**:
   Defines the strict output format required for the downstream pipeline.

Write a Python script at `/home/user/query_pipeline.py` that performs the following steps:
1. Connect to `/home/user/company.db`. Write an optimized SQL query that retrieves:
   - The project name (`project_name`)
   - The project lead's name (`lead_name`)
   - The lead's department name (`department_name`)
   - The number of direct reports the lead has (employees where `manager_id` equals the lead's `id`), named `direct_reports`. Only include projects where the lead has at least 1 direct report. Use proper JOINs and a subquery or aggregation.
2. Load the RDF graph from `/home/user/knowledge.ttl` using `rdflib`.
3. For each row returned by the SQL query, construct a parameterized SPARQL query to find the `ex:riskLevel` of the project based on its `projectName`.
4. Combine the SQL and SPARQL results into a dictionary: `{"project_name": ..., "lead_name": ..., "department_name": ..., "direct_reports": ..., "risk_level": ...}`.
5. Validate each dictionary against the schema in `/home/user/schema.json` using the `jsonschema` library.
6. Write the validated list of dictionaries to `/home/user/report.json` as a JSON array.

You can install `rdflib` and `jsonschema` using `pip install rdflib jsonschema`. Run your script to generate `/home/user/report.json`.