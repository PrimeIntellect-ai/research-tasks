I need you to build a specific ETL pipeline step using Python. We have an undocumented legacy SQLite database at `/home/user/data/legacy_system.db` that contains our internal module registry and their dependency links. 

Your task is to reverse-engineer the schema of this database, extract a materialized view of the dependency graph for active modules, perform sorting and pagination, and export the exact results to a JSON file.

Here are the requirements:
1. **Explore the Database:** Connect to `/home/user/data/legacy_system.db` and figure out the tables. There is a table for modules (containing a status field) and a table for the directional links (dependencies) between them.
2. **Filter:** Ignore any modules whose status is exactly `'deprecated'`. A link is only valid if *both* the source and target modules are active (not deprecated).
3. **Graph Projection & Metrics:** For every active module, calculate its `in_degree` (the number of valid incoming links from other active modules). 
4. **Sort & Paginate:** Sort the active modules based on their `in_degree` in descending order. If there is a tie, sort alphabetically by the module's name in ascending order. We only want the first "page" of results, where page 1 has a limit of exactly 3 modules.
5. **Export:** Write a Python script `/home/user/etl_pipeline.py` that executes this logic and saves the output to `/home/user/output/top_modules_graph.json`. Ensure the output directory exists.

The output JSON must strictly match this structure:
```json
{
  "page": 1,
  "limit": 3,
  "total_active_modules": <integer, total count of non-deprecated modules>,
  "results": [
    {
      "module_name": "<string>",
      "in_degree": <integer>,
      "incoming": ["<string>", "<string>"], 
      "outgoing": ["<string>"]
    }
  ]
}
```
*Note for the lists in `results`: Both `incoming` and `outgoing` arrays must contain the names of the connected active modules, and these arrays must be sorted alphabetically.*

Please set up your script and run it so that the final output JSON is generated correctly.