You are a database administrator tasked with optimizing and standardizing query results derived from multiple data sources. We have relational data representing our workforce and a document store export representing their communication interactions. You need to write a Go program to materialize a graph representation, compute graph metrics, and extract a specific slice of the results.

Here is the setup:
1. A relational SQLite database exists at `/home/user/data.db` with a table `users` (`id INTEGER PRIMARY KEY`, `name TEXT`, `department TEXT`).
2. A JSON file exists at `/home/user/interactions.json` containing communication interactions. The JSON is an array of objects in the format: `[{"src": <user_id>, "dst": <user_id>, "weight": <integer>}, ...]`.

Your objective is to write and execute a Go program at `/home/user/process_graph.go` that performs the following steps:
1. **Cross-representation Mapping & Graph Materialization**: Load the users from the SQLite database and the interactions from the JSON file to build an in-memory graph.
2. **Graph Analytics**: Calculate the **weighted degree centrality** for each user. In this context, a user's weighted degree centrality is the sum of the `weight` of all interactions where they are either the `src` or the `dst`.
3. **Filtering**: Drop any users from the result set whose weighted degree centrality is STRICTLY LESS THAN 10.
4. **Result Sorting**: Sort the remaining users by their weighted degree centrality in DESCENDING order. If two users have the exact same centrality score, break the tie by sorting their `name` in ASCENDING alphabetical order.
5. **Pagination**: Implement pagination on the sorted results using a **page size of 3**.
6. **Output**: Extract **Page 2** (assume 1-indexed pages, so this means items 4, 5, and 6 from the sorted filtered list). Write this exact page to `/home/user/output_page2.json` as a JSON array of objects with the following schema:
   `[{"id": <integer>, "name": "<string>", "centrality": <integer>}, ...]`

You may initialize a Go module in `/home/user` and use external drivers (like `github.com/mattn/go-sqlite3`) to complete the task. Run your program to generate the output file.