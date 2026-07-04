You are a database administrator working on a custom graph database analytics pipeline. We have a Rust-based tool called `cypher_analyzer` that parses cypher-like edge creation queries from our application logs and calculates basic degree centrality (in-degree and out-degree) for each node. It exports this data as a JSON dictionary.

However, the tool is currently broken. The original developer hardcoded the parsing logic to only work with single-digit node IDs, but our database now uses multi-digit IDs. Furthermore, the build configuration seems to be missing a required dependency.

Your task:
1. Navigate to the vendored package located at `/app/cypher_analyzer`.
2. Inspect `src/main.rs` to reverse engineer the expected data model and query format. The tool expects lines on standard input formatted exactly like:
   `MATCH (n1:Person {id: X})-[:KNOWS]->(n2:Person {id: Y})`
   where `X` and `Y` are positive integers of any length.
3. Fix the parsing logic in `src/main.rs` to correctly extract any integer ID (not just single digits).
4. Fix any broken configurations in `Cargo.toml` so the project compiles.
5. Compile the fixed project and place the final executable at `/home/user/cypher_analyzer_fixed`.

The executable must read lines from standard input until EOF, and print a single compacted JSON object to standard output representing the degree centralities. For example, if the input is:
`MATCH (n1:Person {id: 12})-[:KNOWS]->(n2:Person {id: 450})`
It should output:
`{"12":{"in":0,"out":1},"450":{"in":1,"out":0}}`

Automated tests will run your binary with various randomized inputs to ensure it accurately matches our reference oracle.