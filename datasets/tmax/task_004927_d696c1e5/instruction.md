You are assisting a compliance officer auditing an organization's access control systems. You have been provided with an export of relational access logs, but the compliance policies dictate rules based on indirect graph-based relationships (similar to Cypher `MATCH (a)-[*1..3]->(b:SecureVault)`). 

Your task is to map this relational data into an in-memory graph representation using an efficient indexing strategy, and query it to find indirect access violations.

Write a C++ program at `/home/user/audit.cpp` that does the following:
1. Reads the CSV file `/home/user/access_log.csv`. The file has no header. Each line is formatted as `Source,Target` representing a directed access grant from `Source` to `Target`.
2. Builds a directed graph in memory. You must implement an efficient string-to-node indexing strategy (e.g., hash map) to map the entity names to graph vertices.
3. Performs a graph traversal to find ALL entities (nodes) that have a directed path to the node exactly named `SecureVault` with a path length between 1 and 3 edges (inclusive).
4. Writes the names of all entities that satisfy this condition to `/home/user/compliance_violations.txt`.
   - Each entity name must be on a new line.
   - The list must be sorted alphabetically in ascending order.
   - The list must not contain duplicates.
   - Do not include `SecureVault` itself in the output unless it has a cycle back to itself within 3 hops (it doesn't in this dataset).

Compile your program using `g++ -std=c++17 -O3 /home/user/audit.cpp -o /home/user/audit` and execute it to generate the output file.