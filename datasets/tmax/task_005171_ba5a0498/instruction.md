You are assisting a researcher who is organizing a large dataset of graph queries (Cypher) for a knowledge graph derived from video observations.

Your objective has two parts:

**Part 1: Video Artifact Extraction**
The researcher has recorded a dashboard visualization of the evolving graph, saved at `/app/graph_record.mp4`. At exactly 00:00:04 into the video, a brief text overlay flashes on the screen containing a "Secret Node ID" in the format `NODE_ID_XXXX` (where XXXX is a 4-digit number). 
Extract this Secret Node ID from the video. You may use tools like `ffmpeg` to extract frames and `tesseract` (you may need to install `tesseract-ocr`) to read the text.

**Part 2: Cypher Query Filter**
The researcher is accepting community-submitted Cypher queries but wants to avoid a common mistake: queries that return wrong results or explode in memory due to an implicit cross join (Cartesian product). For example, `MATCH (a:Person), (b:Company) RETURN a, b` creates a Cartesian product because there is no relationship connecting `a` and `b`, nor a `WHERE` clause filtering them together.

Write a Python script `/home/user/query_filter.py` that takes a directory path as a command-line argument, reads all `.cypher` files in that directory, and determines if each query is "safe" or "evil".
- A query is "evil" if it contains a `MATCH` clause with multiple disconnected nodes/patterns separated by commas (e.g., `MATCH (a), (b)`) without an explicit relationship like `(a)-->(b)` or `(a)-[]-(b)` in the same match block. (For simplicity, assume any query with a comma-separated list of disconnected nodes in a single `MATCH` clause is evil, unless it is a single path pattern).
- A query is "safe" if all `MATCH` clauses contain explicitly connected graph patterns (e.g., `MATCH (a:Person)-[:KNOWS]->(b:Person)` or `MATCH (n)`).

Your script must print the filename of only the "safe" files to standard output, one per line.

**Final Output**
Create a JSON file at `/home/user/result.json` with the following structure:
```json
{
  "secret_node_id": "NODE_ID_XXXX",
  "filter_script_path": "/home/user/query_filter.py"
}
```