You are a database administrator tasked with optimizing and sanitising a set of graph materialization queries before they are executed against our NoSQL backend. Users submit queries as a simple JSON Lines graph projection DSL. However, some users submit queries that violate the schema, traverse non-existent edges, or exceed the maximum allowed depth, which can cause severe performance issues or crashes.

You have been provided with an image of the graph database schema and rules at `/app/schema.png`. 

Your task:
1. Extract the schema rules (allowed edges and maximum depth) from the image at `/app/schema.png`.
2. Write a Go program at `/home/user/sanitiser.go` and compile it to `/home/user/sanitiser`.
3. The executable must take exactly one argument: the path to a JSON Lines file containing queries.
4. Each line in the file is a JSON object with this structure:
   `{"id": "query_id_here", "path": ["NodeA", "EdgeX", "NodeB"]}`
5. The `path` array represents a graph traversal. It must:
   - Alternatingly specify Nodes and Edges, starting and ending with a Node (e.g., length must be odd and >= 1).
   - Only traverse edges that strictly conform to the allowed directional edges in the schema image.
   - Not exceed the MAX DEPTH specified in the schema image. (Depth is the number of edges in the path; a single node has depth 0).
   - If a path is valid, print its `id` to `stdout` (one ID per line). If invalid, print nothing for that query.

Compile your Go program so it is ready to be executed as `/home/user/sanitiser <input_file.jsonl>`. You may use basic OCR tools like `tesseract` (preinstalled) to read the image, or simply read it yourself to hardcode the rules in your Go script.

Do not output anything else to stdout other than the valid query IDs.