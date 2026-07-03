You are a Data Engineer tasked with building an ETL pipeline that bridges document-oriented data and graph-based analysis. 

We have exports from our NoSQL document store representing employees and projects. You need to write a Python script that parses these documents, builds an in-memory graph to resolve organizational hierarchies, aggregates skillsets across project teams, validates the output against a strict schema, and exports the results.

**Input Data:**
The data is located in `/home/user/data/` (you will need to process these files):
1. `employees.jsonl`: Each line is a JSON document representing an employee.
   - Example: `{"emp_id": "E1", "name": "Alice", "manager_id": "E3", "skills": ["python", "bash"]}`
   - Note: `manager_id` can be `null` if the employee has no manager.
2. `projects.jsonl`: Each line is a JSON document representing a project.
   - Example: `{"proj_id": "P1", "name": "BackendRewrite", "members": ["E1", "E2"]}`

**Your ETL Pipeline Requirements:**
Write a Python script (e.g., at `/home/user/pipeline.py`) that performs the following steps:
1. Load the JSONL files into memory. You may install and use the `networkx` library to build a graph representation of the employees, managers, and projects.
2. For each project, compute the following aggregated arrays:
   - `team_skills`: A deduplicated list of all skills possessed by the direct `members` of the project.
   - `manager_oversight_skills`: A deduplicated list of skills possessed by the *direct managers* of the project members, **excluding** any skills already present in the `team_skills` array.
3. Both `team_skills` and `manager_oversight_skills` arrays must be sorted alphabetically in ascending order.
4. Validate each resulting project summary record against the following JSON schema using the Python `jsonschema` library (you may need to install it):
   ```json
   {
     "type": "object",
     "properties": {
       "proj_id": {"type": "string"},
       "proj_name": {"type": "string"},
       "team_skills": {
         "type": "array",
         "items": {"type": "string"}
       },
       "manager_oversight_skills": {
         "type": "array",
         "items": {"type": "string"}
       }
     },
     "required": ["proj_id", "proj_name", "team_skills", "manager_oversight_skills"],
     "additionalProperties": false
   }
   ```
5. Export the successfully validated records to `/home/user/output/enriched_projects.jsonl`, where each line is a valid JSON object. The output file must be sorted by `proj_id` in ascending order (i.e., process the projects in order of their `proj_id` or sort them before writing).

Ensure your script runs successfully and creates the final `/home/user/output/enriched_projects.jsonl` file. Do not leave debug print statements in the final JSONL output file.