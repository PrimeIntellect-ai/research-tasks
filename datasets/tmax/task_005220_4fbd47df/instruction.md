You are acting as a Database Administrator optimizing a data extraction pipeline. 

Your team relies on a custom-compiled version of SQLite3 to process graph datasets (nodes and edges exported as CSV files) to compute relationship mappings. However, the pipeline is currently broken in two ways:

1. **Environment Setup (Vendored Package):**
   The source code for our specific SQLite3 distribution is located at `/app/sqlite-autoconf`. Recently, a junior developer accidentally introduced a typo into the `Makefile.in` file, causing the build to fail. 
   - Locate the source code in `/app/sqlite-autoconf`.
   - Identify and fix the build perturbation.
   - Compile the tool by running `./configure` and `make`. The resulting executable should be located at `/app/sqlite-autoconf/sqlite3`.

2. **Result Processing & Query Optimization:**
   The current Bash script we use to process the graph data contains a severe performance bug. It generates a SQL query with an implicit cross join when trying to map edge IDs to node names, resulting in a Cartesian product explosion and incorrect results.

   Write a new Bash script at `/home/user/graph_join.sh` that takes exactly two arguments:
   - `$1`: The path to `nodes.csv` (Columns: `id,name,weight`)
   - `$2`: The path to `edges.csv` (Columns: `source_id,target_id,relation`)

   Your script must:
   - Use the compiled SQLite3 binary at `/app/sqlite-autoconf/sqlite3`.
   - Import the provided CSV files into temporary tables.
   - Execute an optimized SQL query using proper explicit `JOIN`s to retrieve the `source_name`, `target_name`, and `relation` for every edge.
   - The output must be perfectly formatted CSV data (with a header row `source_name,target_name,relation`).
   - The results must be sorted alphabetically first by `source_name`, then by `target_name`, and finally by `relation`.
   - Print the CSV output directly to standard output.

Ensure your Bash script handles the arguments dynamically and strictly avoids cross joins. Your script will be tested against randomly generated graph CSV files to ensure bit-exact equivalence with our reference implementation.