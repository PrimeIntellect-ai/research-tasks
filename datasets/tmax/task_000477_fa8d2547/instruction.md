You are a data engineer working on an ETL pipeline that processes NoSQL graph database dumps. Your team recently received a set of routing paths extracted from a graph, but they contain dirty data, schema violations, and paths that violate a new business constraint.

Your manager left a sticky note with the new routing constraints. It has been scanned and saved to `/app/routing_memo.png`. 

Your task is to create a C++ utility that acts as a strict filter (classifier) for these JSON-formatted graph paths. 

**Requirements:**
1. **Extract the Business Rules:** Use `tesseract` (which is pre-installed) to read the text from `/app/routing_memo.png`. This image contains a specific rule regarding forbidden nodes and maximum allowed graph traversal costs.
2. **Write a C++ Validator:** Create a C++ program at `/home/user/validator.cpp` and compile it to `/home/user/validator`. 
   - You may use standard package managers (`apt`) to install `nlohmann-json3-dev` for parsing JSON.
   - The program must read a single JSON line from standard input (`stdin`).
   - The JSON schema for a valid path object is: 
     ```json
     {
       "schema_version": "2.0",
       "path_id": "string",
       "nodes": ["string"],
       "total_cost": integer
     }
     ```
   - The program must **accept** (exit with code `0`) if and only if:
     - The JSON strictly adheres to the schema above (e.g., `schema_version` must be exactly "2.0").
     - The path data satisfies the business constraints extracted from `/app/routing_memo.png`.
   - The program must **reject** (exit with code `1`) if the schema is invalid, fields are missing/wrong type, or the business constraints are violated.

**Testing:**
To complete the task, your compiled executable `/home/user/validator` must flawlessly distinguish between valid and invalid records. We will pipe individual JSON records into your executable like so:
`./validator < record.json`

Ensure your code handles malformed JSON gracefully by rejecting it (exit code 1) rather than crashing.