You are a data analyst dealing with a raw CSV dump from a graph database. The database suffered from a corrupted index, which caused it to output "stale" rows—meaning older versions of edges were exported alongside newer ones. 

Your task is to write a robust Bash script located at `/home/user/process_graph.sh` to clean this CSV data and convert it into Cypher query format for re-ingestion.

**Requirements:**
1. Your script must read a headerless CSV from **standard input (`stdin`)**. The format of each line is `source_id,target_id,timestamp`.
2. Extract the minimum valid timestamp threshold from the image located at `/app/corrupted_threshold.png`. (You can use `tesseract` to read the image).
3. Filter out any rows where the `timestamp` is *strictly less* than the threshold found in the image.
4. Filter out any self-loops (where `source_id` equals `target_id`).
5. Deduplicate edges: For any directed pair of `(source_id, target_id)`, keep only the edge with the **highest** `timestamp`.
6. Convert the remaining valid edges into Cypher `CREATE` statements with the exact following format:
   `CREATE (n<source_id>)-[:CONNECTED_TO {time: <timestamp>}]->(n<target_id>);`
7. The final output printed to `stdout` must be sorted alphabetically.

**Example Input (stdin):**
```text
10,20,1625000050
10,20,1625000010
30,30,1690000000
40,50,1500000000
```
*(Assume the threshold in the image is 1600000000 for this example)*

**Example Output (stdout):**
```text
CREATE (n10)-[:CONNECTED_TO {time: 1625000050}]->(n20);
```

Ensure your script `/home/user/process_graph.sh` is executable. Automated tests will pipe heavily randomized CSV data into your script and compare its output strictly against a reference implementation.