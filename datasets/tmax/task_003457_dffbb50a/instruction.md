You are a database administrator tasked with recovering and optimizing a custom in-memory graph query engine. A recent system failure destroyed the active graph dataset, but a screen recording of the database transaction monitor was saved. You must recover the dataset from the video, parse it, and then massively optimize the query engine to meet strict latency SLAs.

**Part 1: Data Recovery**
You are provided with a video file at `/app/transaction_monitor.mp4`. This video is a screen recording of a terminal that was printing a stream of edge insertions into the graph database. 
1. Use tools like `ffmpeg` and `tesseract-ocr` (which you can install if needed) to extract the frames and read the text.
2. The text in the video contains lines in the format: `INSERT_EDGE: <node_u> -> <node_v>`.
3. Parse the extracted text to reconstruct the graph and save it as a clean CSV file at `/home/user/edges.csv` with the format `u,v` on each line. Ignore any OCR noise or partial lines.

**Part 2: Query Plan Optimization**
The current query engine is written in C and is located at `/home/user/query_engine.c`. It reads `edges.csv` and executes a hard-coded query equivalent to the following Cypher + Window function logic:
```cypher
MATCH (a)-[:KNOWS]->(b)-[:KNOWS]->(c)
WITH a, count(c) as path_count
ORDER BY a.id
RETURN a.id, sum(path_count) OVER (ORDER BY a.id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_sum
```
However, the current C implementation uses a naive execution plan: it stores edges in a flat array and performs nested table scans (O(E^2) complexity) to find length-2 paths, followed by an unoptimized rolling sum calculation.

Your task is to:
1. Rewrite `/home/user/query_engine.c` to optimize the query execution plan. You should implement an efficient graph index (e.g., an adjacency list) to reduce the path-finding complexity to O(V + E).
2. Maintain the exact same output format. The program must print the final aggregated result to `stdout`.
3. Compile your optimized code into an executable at `/home/user/query_engine_opt`.

**Part 3: Verification**
To pass this task, your optimized C engine must output the mathematically correct result for the recovered graph, and it must do so extremely quickly. A verifier script will measure the execution time of `/home/user/query_engine_opt` on a much larger hidden dataset to ensure your algorithm achieves the required algorithmic speedup. 

Create a log file at `/home/user/optimization_report.txt` detailing the big-O complexity of your new execution plan compared to the old one.