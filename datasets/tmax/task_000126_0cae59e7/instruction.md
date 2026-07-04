You are acting as a compliance officer auditing an IT system. We suspect that an internal reporting tool generated an access audit report using a flawed SQL query containing an implicit cross join, inflating the privileges users actually hold.

You are provided with two files representing the system's state:
1. **`/home/user/audit.db`**: A SQLite database containing the table `reported_access(user_id TEXT, resource_id TEXT)`. This is the output of the flawed reporting tool.
2. **`/home/user/graph.json`**: A JSON file exporting the ground-truth access control graph. It has the following schema:
   ```json
   {
     "nodes": [
       {"id": "U1", "type": "User"},
       {"id": "R1", "type": "Role"},
       {"id": "RES1", "type": "Resource"}
     ],
     "edges": [
       {"source": "U1", "target": "R1", "relation": "HAS_ROLE"},
       {"source": "R1", "target": "RES1", "relation": "CAN_ACCESS"}
     ]
   }
   ```

A user *actually* has access to a resource only if there is a valid path in the graph: `User -> HAS_ROLE -> Role -> CAN_ACCESS -> Resource`.

**Your task:**
Write and execute a Go program at `/home/user/audit.go` that:
1. Parses the true access permissions from the graph representation (`/home/user/graph.json`).
2. Queries the relational representation (`/home/user/audit.db`) for all reported access pairs.
3. Cross-references the two data sources to identify "violations" (pairs present in the SQLite database but NOT valid according to the graph).
4. Exports the results to `/home/user/violations.json` as a JSON array of objects, structured exactly like this:
   ```json
   [
     {"user_id": "U1", "resource_id": "RES2"},
     {"user_id": "U2", "resource_id": "RES1"}
   ]
   ```
   The array must be sorted alphabetically by `user_id`, and then by `resource_id`.

Ensure your Go program is completely self-contained, runs successfully, and creates the required output file. You will need to initialize a go module and fetch the SQLite driver (`github.com/mattn/go-sqlite3`) to complete this task.