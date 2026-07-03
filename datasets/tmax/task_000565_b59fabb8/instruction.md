You are acting as a data analyst. You have been provided with two CSV files representing a relational dependency graph of software components. 

The files are located at:
1. `/home/user/nodes.csv` - Contains the components. Columns: `id,name`
2. `/home/user/edges.csv` - Contains directed dependencies. Columns: `parent_id,child_id` (meaning `parent_id` depends on `child_id`).

Your task is to write and execute a Go program (`/home/user/analyze.go`) that does the following:
1. Parses both CSV files.
2. Constructs an in-memory graph.
3. Performs a recursive traversal to find *all* transitive dependencies (every component reachable downwards in the dependency tree) for the component named `Core_System`.
4. Maps the resulting component IDs back to their names.
5. Writes the unique names of all these transitive dependencies to a file at `/home/user/core_deps.txt`.

The output file `/home/user/core_deps.txt` must contain exactly one component name per line, sorted alphabetically. Do not include `Core_System` itself in the output, only its dependencies. 

Use standard Go libraries only. You can run your program using `go run /home/user/analyze.go`.