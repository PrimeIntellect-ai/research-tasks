You are a data engineer building an ETL pipeline to migrate and analyze knowledge graph data. 

You have been provided with an N-Triples file located at `/home/user/graph.nt` containing social network data. The relations included are `<follows>` and `<knows>`.

Your task consists of two parts:

**Part 1: Graph Query Formulation**
Write a valid SPARQL query that finds all pairs of subjects `?x` and `?y` such that:
1. `?x` follows `<http://example.org/TargetUser>`
2. `?y` follows `<http://example.org/TargetUser>`
3. `?x` knows `?y`

Save this SPARQL query exactly as written into the file `/home/user/query.rq`.

**Part 2: Go-based ETL and Indexing**
Since we are migrating to a relational schema for local processing, you need to implement this pipeline in Go.
Write a Go program at `/home/user/etl.go` that does the following:
1. Reads `/home/user/graph.nt` and loads all triples into a SQLite database located at `/home/user/graph.db`. The table must be named `triples` with columns `subject`, `predicate`, and `object`.
2. Implements an **index strategy** by creating the necessary SQL indexes on the `triples` table to highly optimize the execution of the graph query from Part 1. 
3. Executes the SQL equivalent of your SPARQL query against the SQLite database.
4. Exports the resulting pairs into a CSV file located at `/home/user/result.csv`. 

**CSV Format Requirements:**
- The CSV must have a header: `user1,user2`
- `user1` corresponds to `?x` and `user2` corresponds to `?y`.
- The rows must be sorted alphabetically by `user1` in ascending order, and then by `user2` in ascending order.
- Remove the angle brackets (`<` and `>`) from the URIs in the CSV output.

**Environment details:**
- You can initialize a Go module in `/home/user` and use `github.com/mattn/go-sqlite3` for database operations.
- Ensure your Go script handles basic error checking and runs cleanly. Do not leave the database locked.