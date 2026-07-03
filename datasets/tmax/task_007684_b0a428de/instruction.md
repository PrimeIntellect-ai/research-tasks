You are a data analyst investigating a dataset of entity relationships. You have been provided with a CSV file at `/home/user/graph_data.csv` containing knowledge graph triples in the format `subject,predicate,object`. 

We previously stored this in an SQLite database, but a corrupted index is causing stale rows to be returned. We need you to bypass the broken database, process the raw CSV data using Python, and extract a specific relationship pattern.

Write a Python script at `/home/user/query_graph.py` that does the following:
1. Reads `/home/user/graph_data.csv`.
2. Loads the data into a temporary/in-memory SQLite database to perform query operations.
3. Constructs a **parameterized SQL query** to perform a knowledge graph pattern match. You must find all `Company` entities that satisfy the following exact graph pattern:
   `Person(name=?)` -> `works_for` -> `Company` <- `produced_by` <- `Product` <- `purchased` <- `Person(name=?)`
4. The script should accept exactly two command-line arguments: the name of the first person (who works for the company) and the name of the second person (who purchased the product).
5. When executed, the script should output the matching `Company` names (the objects of the `works_for` relationship) to `/home/user/pattern_results.txt`. The company names must be written one per line, sorted alphabetically. 

Once your script is written, execute it using the arguments `"Alice"` and `"Bob"`.

Ensure your results are strictly in `/home/user/pattern_results.txt`.