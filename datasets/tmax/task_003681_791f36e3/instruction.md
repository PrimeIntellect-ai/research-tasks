You are a data engineer responsible for a graph-processing ETL pipeline. The pipeline computes the shortest path from a specific root node (`node_0`) to all other reachable nodes in a directed graph using SQL recursive CTEs.

Recently, our infrastructure was isolated (no internet access), and we had to vendor the source code for our database engine, SQLite3, into the container. However, the build is failing, and our ETL script is producing wildly incorrect results (and sometimes running out of memory) due to an implicit cross join in the SQL query.

Your objectives:

1. **Fix and Build the Vendored Database Tool:**
   We have vendored the SQLite source amalgamation at `/app/sqlite-amalgamation-3430000`. It contains a custom `Makefile`. Currently, running `make` fails due to a missing linker flag. Find the `Makefile`, fix the compiler perturbation (it's missing a standard library link flag for dynamic linking required by SQLite on Linux), and build the `sqlite3` binary successfully. 

2. **Fix the ETL Script:**
   The wrapper script is located at `/home/user/etl.sh`. It takes exactly one argument: the path to an input CSV file containing graph edges (columns: `source,target`). 
   The script currently uses the newly built SQLite binary to load the CSV, compute shortest paths from `node_0`, and output the results. 
   However, the `WITH RECURSIVE` CTE in the script has a severe logic bug: the recursive step performs an implicit cross join without a proper `WHERE` or `ON` clause, leading to a Cartesian product explosion instead of graph traversal.

   Modify `/home/user/etl.sh` so that:
   - It correctly computes the shortest path (minimum depth) from `node_0` to all reachable nodes (including `node_0` itself at depth 0).
   - It outputs the result as a CSV to standard output with columns `node,shortest_path`, strictly ordered by `node` ascending.
   - It references the newly compiled binary at `/app/sqlite-amalgamation-3430000/sqlite3`.

Ensure `/home/user/etl.sh` is executable and prints the bit-exact expected CSV output so it can pass our automated fuzzer, which will test it against random edge lists.