You are a database reliability engineer tasked with recovering a critical network routing graph from a corrupted SQLite backup. The graph database `/app/routing_backup.db` contains two tables: `nodes` (id, name) and `edges` (source_id, target_id, weight). However, the index `idx_edges_source` is corrupted and occasionally returns stale, ghost rows that create phantom paths.

Additionally, our network monitoring system recorded a critical alert audio file located at `/app/alert.wav`. This audio contains the names of several hardware nodes that have caught fire and are completely offline. 

Your objective is to build a robust pathfinding script that can reliably compute the shortest path between any two nodes, completely avoiding the offline nodes mentioned in the audio file and bypassing the corrupted index.

Specifically, you must:
1. Transcribe the audio file `/app/alert.wav` to identify the names of the offline nodes.
2. Write a Python script at `/home/user/route_calculator.py` that takes exactly two arguments: the names of a starting node and an ending node (e.g., `python3 /home/user/route_calculator.py "NodeAlpha" "NodeOmega"`).
3. The script must query `/app/routing_backup.db` to project the graph, but it must force SQLite to ignore the corrupted index (or query in a way that avoids it) so no phantom edges are used.
4. The script must implement a shortest-path graph traversal (using Dijkstra's or similar) to find the minimum total weight path from the start to the end node.
5. The path MUST NOT traverse any of the offline nodes identified from the audio alert.
6. If a path exists, the script should print the total minimum weight as a single integer to `stdout`. If no path exists, print `-1`.
7. Your script should be optimized to respond within 100ms per execution, which may require you to programmatically define a new, uncorrupted index in the database on your first run.

Ensure your script is self-contained and relies only on Python standard libraries or easily installable packages (like `whisper` for the transcription step, though you can hardcode the transcribed offline nodes in your final script once you figure them out).