You are assisting a compliance officer in auditing a company's internal access systems. The company's identity and access management (IAM) graph database has been taken offline for maintenance, but a raw export of the graph is available in `/home/user/audit_data/`.

The export consists of two files:
1. `/home/user/audit_data/nodes.json` - Contains the nodes of the graph (Employees and Systems).
2. `/home/user/audit_data/edges.json` - Contains the relationships (`MANAGES` and `HAS_ACCESS`).

Your task is to identify Segregation of Duties (SoD) violations. The SoD policy strictly dictates that no employee may have access to both "Financial_Records" and "Audit_Logs".
Crucially, access is inherited: if Employee A `MANAGES` Employee B, Employee A transitively inherits all of Employee B's access rights (and anyone Employee B manages, and so on).

Perform the following steps:
1. Reverse-engineer the data model from the JSON files to understand the exact structure, property names, and target node identifiers for "Financial_Records" and "Audit_Logs".
2. Create a Rust project in `/home/user/auditor`.
3. Write a Rust program in this project that parses the JSON files, materializes the projected access graph in memory (designing a fast indexing/traversal strategy to find reachable systems from each employee), and identifies all employees violating the SoD policy.
4. Run your Rust program to generate the results.
5. Save the IDs of all violating employees to `/home/user/violations.txt`, with one ID per line, sorted alphabetically.
6. To aid the compliance team once the database is back online, write the equivalent Cypher query that would return the IDs of the violating employees. Save this query to `/home/user/query.cypher`.

You can use standard shell commands and `cargo` to create and run your Rust project. You may add any necessary standard dependencies (like `serde`, `serde_json`) to your `Cargo.toml`.