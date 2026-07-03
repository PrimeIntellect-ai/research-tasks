You are an AI assistant helping a researcher organize and extract datasets from a local knowledge graph of academic papers.

The researcher has an SQLite database containing the knowledge graph at `/home/user/dataset.sqlite`. Unfortunately, the database suffered a partial corruption during a recent power failure. Specifically, the researcher suspects that an index on the citation relationships table is corrupted, causing it to return stale or missing rows when queried. 

Additionally, the researcher has been writing a custom Go tool to export hierarchical citation graphs, but they left it in a broken state. The source code for this tool is vendored locally at `/app/kg-exporter-1.0.0`. It does not require an internet connection to build, as all dependencies are already vendored, but it currently fails to compile due to a configuration error. Even when forcefully compiled, the recursive graph traversal logic (CTE) has a bug and traverses the graph in the wrong direction.

Your objectives are:
1. **Fix the Database:** Inspect `/home/user/dataset.sqlite`. Reverse engineer the schema to identify the tables for papers and citations. Identify and rebuild the corrupted index so that queries return the correct, complete relationships.
2. **Fix the Vendored Package:** 
   - Inspect `/app/kg-exporter-1.0.0`. 
   - Fix the build perturbation (the `Makefile` or build scripts are misconfigured, preventing the SQLite CGO driver from compiling).
   - Fix the SQL logic inside the Go code. It is supposed to use a recursive query (CTE) to find the root paper and all papers it cites, up to a specified maximum depth. Currently, it traverses backward (finding papers that cite the root) or has malformed join conditions.
3. **Compile and Deploy:** Build the corrected package and place the executable at `/home/user/kg-export`.

**Executable Specification:**
The compiled binary must function exactly as follows:
`./kg-export <db_path> <root_paper_id> <max_depth>`
- `<db_path>`: Absolute path to the SQLite database.
- `<root_paper_id>`: The ID of the paper to start the traversal from.
- `<max_depth>`: The maximum recursive depth (0 means just the root paper, 1 means the root and papers it directly cites, etc.).
- **Output:** The program must print a strictly formatted JSON array of integers representing the unique paper IDs in the traversed graph (including the root). The array MUST be sorted in ascending order. No other text or logging should be printed to standard output. Example: `[12, 45, 102, 304]`

Do not rely on downloading external packages; use the vendored workspace.