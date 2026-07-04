You are tasked with securing a legacy graph and aggregation analytics engine for a data analysis pipeline. 

As a data analyst, you process large, complex CSV files representing transaction networks. Your primary tool is a custom, proprietary compiled query engine located at `/app/graph_engine`. This engine accepts a target CSV dataset and a JSON-formatted query pipeline (similar to NoSQL aggregation pipelines) to execute complex joins, subqueries, and graph analytics (like centrality calculation and graph clustering) directly against the CSV data.

However, the `/app/graph_engine` binary has several critical security vulnerabilities: it lacks resource bounding. Certain query pipeline configurations, specifically unbounded recursive graph traversals and deeply nested Cartesian joins, cause the binary to hang, exhaust memory, or crash. Malicious actors have begun submitting engineered JSON query payloads disguised as standard analytics tasks.

Your objective is to build a pre-execution sanitizer in Rust that acts as a gatekeeper for these JSON query pipelines.

Requirements:
1. Create a new Rust project at `/home/user/query_sanitizer`.
2. Write a Rust application that accepts a single file path as a command-line argument: `./query_sanitizer <path_to_json_query>`.
3. The sanitizer must parse the JSON file and determine if it is safe to pass to the engine.
4. If the query is safe, the application must print `SAFE` to `stdout` and exit with code 0.
5. If the query is malicious (will crash the engine), it must print `EVIL` to `stdout` and exit with code 1.
6. The compiled binary must be located at `/home/user/query_sanitizer/target/release/query_sanitizer`.

To help you determine the exact patterns that crash the engine, the stripped binary is provided at `/app/graph_engine`. You can use it as a black-box oracle by fuzzing it or reverse-engineering it with preinstalled tools (`objdump`, `strings`, `gdb`). You also have access to two directories:
- `/app/data/clean_samples/`: Examples of valid, safe JSON queries.
- `/app/data/evil_samples/`: Examples of queries known to crash the engine.

Analyze the engine and the samples to deduce the precise NoSQL pipeline parameters and join/graph nesting constraints. Once deployed, an automated suite will verify your sanitizer against hidden datasets.