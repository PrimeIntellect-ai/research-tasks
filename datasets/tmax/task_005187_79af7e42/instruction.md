You are acting as an AI assistant for a Compliance Officer auditing an enterprise system for privilege escalation vulnerabilities. 

We have extracted system access logs and permission structures from a NoSQL document store and mapped them into a local relational database: `/home/user/audit.db` (SQLite3 format).

The database contains a mapped graph structure representing identities and their relationships.
Schema:
- Table `nodes`: `id` (VARCHAR), `type` (VARCHAR - either 'USER' or 'ROLE'), `risk_weight` (INTEGER)
- Table `edges`: `src` (VARCHAR), `dst` (VARCHAR), `rel_type` (VARCHAR - 'ASSUMES', 'INHERITS', or 'CAN_MODIFY')

**Your Task:**
Write a C program that queries this database to identify critical privilege escalation paths and outputs a JSON report. 

1. **Graph Query Mapping:** You must find all paths in the graph that match the following Cypher-like pattern:
   `(u1:USER)-[:ASSUMES]->(r1:ROLE)-[:INHERITS]->(r2:ROLE)-[:CAN_MODIFY]->(u2:USER)`
   Where `u1` is NOT the same as `u2`.

2. **Analytical Aggregation:** For each matching path, calculate the `path_risk`, defined as the sum of the `risk_weight` of all four nodes in the path (`u1`, `r1`, `r2`, `u2`).
   Because users can be compromised via multiple paths, the compliance officer only wants to see the *highest risk path* for each vulnerable target user (`u2`). Use SQL window functions or aggregations in your query to filter the results so that only the single path with the maximum `path_risk` per `u2` is returned. If there is a tie in `path_risk` for a target user, resolve it by selecting the path with the alphabetically first `u1` id.

3. **Implementation & Output:**
   - Write your program in `/home/user/audit.c`.
   - Your code must connect to the SQLite database natively using the SQLite C API. (You may need to install `libsqlite3-dev` and compile with `-lsqlite3`).
   - Compile the program to an executable named `/home/user/audit_tool`.
   - When run, `/home/user/audit_tool` must generate a strictly formatted JSON array in `/home/user/violations.json`.

**JSON Output Format:**
The output must be a valid JSON array of objects. Each object must have the following exact schema, ordered alphabetically by `target_user`:
```json
[
  {
    "target_user": "user_id_here",
    "source_user": "source_user_id_here",
    "path_risk": 150
  }
]
```

Write the code, compile it, and run it to produce the final `violations.json` file.