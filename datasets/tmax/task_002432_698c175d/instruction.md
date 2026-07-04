You are a Database Administrator tasked with optimizing a set of slow graph queries that run on a SQLite database.

We have a local graph database built using the `sqlite-utils` library. However, the data pipeline has been running incredibly slowly. 

System State & Requirements:
1. The source code for the pipeline's database library, `sqlite-utils` (version 3.35.1), is vendored at `/app/sqlite-utils`. Our environment is configured to use this vendored version.
2. There is a database generation script at `/home/user/db_setup.py` which builds a graph dataset of nodes and relationships and saves it to `/home/user/graph.db`.
3. We suspect there is a bug in the vendored `sqlite-utils` package that is silently preventing query optimizations (specifically, index creation) from being applied during the database setup.
4. You must locate and fix this bug in `/app/sqlite-utils`.
5. After fixing the bug, re-run `/home/user/db_setup.py` to regenerate `/home/user/graph.db` properly.
6. Finally, write a script `/home/user/optimize_queries.py` that computes the total weight of the shortest path between 50 pairs of nodes specified in `/home/user/pairs.json`.
   - Your script must load the SQLite data and efficiently compute the shortest paths. 
   - The script must save a dictionary mapping the string representation of the pair (e.g., `"12-85"`) to the shortest path weight (an integer) in `/home/user/results.json`. If no path exists, map it to `null`.
7. Your `optimize_queries.py` script must complete in under 2.0 seconds. 

Ensure your final output file `results.json` is perfectly formatted. Do not modify the `db_setup.py` script or `pairs.json` file.