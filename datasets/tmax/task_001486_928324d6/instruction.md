You are acting as a database administrator managing a large knowledge graph stored in an SQLite database at `/home/user/kg.db`. 

The knowledge graph consists of a single table:
`triples(subject TEXT, predicate TEXT, object TEXT)`

Currently, there are no indexes on this table. We need to run a graph pattern matching query to find all specific entities, but the query is exceedingly slow due to the lack of optimization.

Your task is to:
1. Analyze the database and create the optimal index(es) on the `triples` table to speed up lookups filtering by `predicate` and `object`.
2. Execute a SQL query to find all `subject`s that meet ALL of the following conditions simultaneously (Knowledge Graph pattern matching):
   - `predicate` = 'is_a' AND `object` = 'AI_Agent'
   - `predicate` = 'has_skill' AND `object` = 'QueryOptimization'
   - `predicate` = 'assigned_to' AND `object` = 'Project_X'
3. Write a small script (in Python, Bash, or Ruby) to chain the output of your SQL query into a JSON pipeline. The final result should be a JSON array of the matching `subject` names, sorted alphabetically.
4. Save this final JSON array to `/home/user/result.json`.

Ensure the JSON file is exactly in this format (example):
```json
[
  "Entity_A",
  "Entity_B"
]
```

Do not modify the existing data in the `triples` table, only add indexes.