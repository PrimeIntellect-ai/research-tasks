You are an AI assistant helping a researcher organize their dataset of academic publications. The researcher has a SQLite database located at `/home/user/publications.db` containing relational data about authors and the papers they have written. 

The database has two tables:
1. `author (id INTEGER PRIMARY KEY, name TEXT)`
2. `wrote (author_id INTEGER, paper_id INTEGER)`

The researcher needs to project this relational data into a graph format to analyze co-authorship networks, but their current query is too slow. A co-authorship edge exists when two distinct authors have written the same paper.

Your task is to write a Python script at `/home/user/build_graph.py` that does the following:

1. **Query Plan Analysis (Unoptimized)**: Connect to the database and generate the `EXPLAIN QUERY PLAN` output for the following query:
   `SELECT a1.author_id, a2.author_id, count(*) FROM wrote a1 JOIN wrote a2 ON a1.paper_id = a2.paper_id WHERE a1.author_id < a2.author_id GROUP BY a1.author_id, a2.author_id;`
   Save the exact multi-line string output of the plan to `/home/user/plan_unoptimized.txt`.

2. **Query Optimization**: Execute SQL statements within your Python script to create the necessary index(es) on the `wrote` table to optimize the joins and lookups in the query above. 

3. **Query Plan Analysis (Optimized)**: Generate the `EXPLAIN QUERY PLAN` output for the *same* query after your indexes have been created. Save this new plan output to `/home/user/plan_optimized.txt`.

4. **Graph Materialization & Export**: Execute the optimized query to extract the co-authorship edges. Convert this data into a graph representation (JSON format) and save it to `/home/user/coauthors.json`. The JSON file must contain a single array of objects, where each object represents an edge with the format:
   ```json
   [
     {"source": 1, "target": 2, "weight": 1},
     {"source": 3, "target": 5, "weight": 2}
   ]
   ```
   *Note: `source` must be the smaller `author_id`, `target` the larger `author_id`, and `weight` the number of shared papers.*

Execute your Python script so that the three output files (`plan_unoptimized.txt`, `plan_optimized.txt`, and `coauthors.json`) are generated in `/home/user/`.