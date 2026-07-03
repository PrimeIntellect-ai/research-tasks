You are a database administrator tasked with optimizing a critical data retrieval pipeline for our knowledge graph. 

First, we received an automated voice alert that contains the name of a compromised server node in our infrastructure. An audio recording of this alert is located at `/app/alert.wav`. You must transcribe this audio to determine the starting node ID (it will be spoken as a string of letters and numbers).

Second, we have a raw data dump of our infrastructure graph exported from our NoSQL document store, located at `/home/user/infrastructure_graph.json`. This file contains nodes and their connections.

Third, our current querying script, located at `/home/user/slow_traversal.py`, is extremely inefficient. It performs naive recursive queries to find the shortest path from a given starting node to the central database node (ID: "DB-CORE-99") while summing up the connection latencies. 

Your objectives are:
1. Extract the starting node ID from `/app/alert.wav`.
2. Rewrite and optimize the traversal script to create `/home/user/fast_traversal.py`. The new script must use efficient graph traversal algorithms (like Dijkstra's or A*) and proper data structures instead of naive recursion. It should take the starting node ID as a command-line argument.
3. The script `/home/user/fast_traversal.py` must output a JSON file at `/home/user/path_result.json` containing exactly:
   - `start_node`: the node ID from the audio.
   - `path`: a list of node IDs forming the shortest path.
   - `total_latency`: the numeric sum of latencies along that path.

Your optimized script will be tested against a much larger dataset. To succeed, `/home/user/fast_traversal.py` must produce the exact same correct result as the original script but achieve a runtime speedup of at least 50x compared to `slow_traversal.py` on the test dataset.

Ensure your Python script is executable, well-commented, and includes any necessary package configurations.