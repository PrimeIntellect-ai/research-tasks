You are a database administrator tasked with implementing a local graph database for a network analysis tool. We are investigating a communication network using a locally embedded graph database called `kuzu`. 

Your task involves writing data ingestion scripts, crafting an optimized Cypher query, and validating the final output against a strict JSON schema.

Here is what you need to do:

1. **Environment Setup**
   Install the `kuzu` graph database library for Python and the `jsonschema` CLI tool. Ensure you're working entirely in `/home/user`.

2. **Graph Database Ingestion**
   We have two raw data files that will be placed in `/home/user/data/` (they already exist):
   - `nodes.csv` (Columns: `id`, `name`, `department`)
   - `edges.csv` (Columns: `src`, `dst`, `relationship`, `weight`)

   Write a Python script at `/home/user/init_graph.py` that:
   - Initializes a Kuzu database in the directory `/home/user/kuzu_db`.
   - Creates a node table `Person` with properties `id INT64` (Primary Key), `name STRING`, and `department STRING`.
   - Creates a relationship table `CommunicatesWith` from `Person` to `Person` with properties `relationship STRING` and `weight DOUBLE`.
   - Uses Kuzu's `COPY` Cypher commands to efficiently load `nodes.csv` and `edges.csv` into the database.

3. **Cypher Query Optimization**
   Write an optimized Cypher query and save it exactly as `/home/user/query.cypher`. 
   The query must:
   - Find all people who are exactly 2 hops away from the person named 'Alice'.
   - Only traverse edges where the `weight` property is **strictly greater than 0.5**.
   - Return the destination person's name as `target_name`, and the sum of the two edge weights as `total_weight`.
   - Order the results by `total_weight` descending, then by `target_name` ascending.
   - Limit the output to the top 5 results.

4. **Execution and Schema Validation**
   Write a bash script at `/home/user/execute_and_validate.sh` that:
   - Uses a small inline Python snippet to execute the query in `/home/user/query.cypher` against the Kuzu DB.
   - Saves the result as a JSON array of objects to `/home/user/output.json`. Example format: `[{"target_name": "Bob", "total_weight": 1.5}]`
   - Validates `/home/user/output.json` against the JSON schema provided at `/home/user/schema.json` using the `jsonschema` CLI.
   - Exits with code 0 if successful.

Make sure your bash script executes properly and produces the correct `output.json`.