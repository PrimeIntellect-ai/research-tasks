You are a data analyst dealing with a project management system. You have been given two CSV files representing tasks and their dependencies. Unfortunately, a user error has introduced a cyclic dependency (a "deadlock") into the task graph, preventing the pipeline from executing.

Your goal is to write a Python script that processes these CSV files, identifies and resolves the cycle, and outputs the corrected hierarchical task structure as a nested JSON file.

Files provided (you must assume these exist):
1. `/home/user/tasks.csv`: Contains `task_id` and `task_name`.
2. `/home/user/dependencies.csv`: Contains `dependent_task`, `prerequisite_task`, and `weight`. (A `dependent_task` cannot start until its `prerequisite_task` is completed).
3. `/home/user/schema.json`: A JSON schema file defining the required output structure.

Your tasks:
1. Parse the CSV files to build a directed graph of task dependencies. The edges should go from `prerequisite_task` to `dependent_task` (representing the flow of execution).
2. Traverse the graph to find the cycle. You are guaranteed there is exactly one simple cycle.
3. Break the cycle by removing the dependency edge (from prerequisite to dependent) that has the **lowest** `weight`.
4. After breaking the cycle, find the "root" tasks (tasks that have no prerequisites).
5. Generate a nested JSON structure starting from the root tasks. Each task should have a `task_id`, `task_name`, and a `dependents` array containing its immediate dependent tasks in the same structure. 
   - If a task has multiple dependents, sort them alphabetically by `task_id`.
   - The root tasks in the main array should also be sorted alphabetically by `task_id`.
   - If a task has no dependents, the `dependents` array must be empty `[]`.
6. Validate your generated JSON against `/home/user/schema.json` using the `jsonschema` Python library (you may need to install it).
7. Save the final JSON to `/home/user/resolved_hierarchy.json`.

Ensure your output exactly strictly matches the structure required by the schema and handles the cycle correctly.