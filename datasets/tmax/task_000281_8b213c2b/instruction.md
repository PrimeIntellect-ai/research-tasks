As a Database Administrator optimizing a graph database, you need to implement a strict query sanitizer for Cypher queries. Malicious or poorly optimized queries have been degrading database performance by performing unbounded traversals or querying non-existent schema relationships.

Your task is to build a C-based query sanitizer that filters out invalid or expensive Cypher queries based on a set of constraints.

**Step 1: Extract Constraints from Video**
We lost the original documentation, but a screen recording of the schema design meeting is available at `/app/schema_meeting.mp4`. 
Use `ffmpeg` to extract the frames and examine them (you can use `tesseract` or manual inspection via terminal output tools if needed, or simply extract strings from the raw video if it's encoded as a text stream, or extract frames and use OCR). 
The video contains two critical pieces of information in one of its frames:
1. `MAX_DEPTH=X` (an integer representing the maximum allowed variable-length path traversal).
2. `ALLOWED SCHEMA:` followed by the exact valid node labels and relationships in the graph (e.g., `(NodeA)-[:REL]->(NodeB)`).

**Step 2: Implement the Sanitizer in C**
Write a C program at `/home/user/query_filter.c` and compile it to `/home/user/query_filter`.
The program must take a single command-line argument: the path to a file containing a Cypher query.
Example invocation: `/home/user/query_filter /path/to/query.cql`

The program must parse the query and apply the constraints extracted from the video:
- **Reject (Exit Code 1):** If the query contains a variable-length relationship (e.g., `[*1..5]`) where the upper bound exceeds the `MAX_DEPTH`.
- **Reject (Exit Code 1):** If the query explicitly defines a pattern with node labels and relationship types that DO NOT exist in the allowed schema (e.g., if `(User)-[:DRIVES]->(Vehicle)` is allowed, but the query uses `(Vehicle)-[:DRIVES]->(User)`, it must be rejected).
- **Accept (Exit Code 0):** If the query adheres to the schema and depth constraints, or if it doesn't specify conflicting labels/depths.

**Step 3: Test Against the Corpora**
We have provided two directories containing test queries:
- `/app/corpus/clean/`: Contains strictly valid, well-optimized queries. Your program MUST accept (exit 0) all of these.
- `/app/corpus/evil/`: Contains queries that either violate the schema or exceed the maximum traversal depth. Your program MUST reject (exit 1) all of these.

You can iteratively refine your C program by testing it against these corpora. Once compiled and working correctly against both sets, your task is complete. Ensure your final executable is located at `/home/user/query_filter`.