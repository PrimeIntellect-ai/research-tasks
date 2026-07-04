You are a data analyst working for a logistics company. You need to build a dynamic routing tool that calculates the shortest path between distribution centers, taking into account real-time outages recorded in a dashboard video feed.

We have a network of 100 distribution nodes (IDs 0 to 99). 
You are provided with two resources:
1. `/app/edges.csv`: A CSV file containing the network topology. Columns are `src` (int), `dst` (int), and `cost` (float). The graph is directed.
2. `/app/node_status.mp4`: A 60-second video (1 frame per second, 60 frames total) recording the status of all 100 nodes over a 60-second period. 

**Video Dashboard Format:**
- Resolution: 100x100 pixels.
- The video represents a 10x10 grid of blocks. Each block is 10x10 pixels.
- Block at Row `R` (0-9) and Column `C` (0-9) corresponds to Node ID = `R * 10 + C`. 
- For example, the top-left 10x10 pixel block is Node 0. The top-right 10x10 pixel block is Node 9.
- If a block is purely White (RGB 255, 255, 255), the node is **ONLINE** at that second.
- If a block is purely Black (RGB 0, 0, 0), the node is **OFFLINE** at that second.
- Time `T` starts at 0 for the first frame (second 0) and ends at 59 for the last frame.

**Your Objective:**
1. **Data Processing & Database Construction:** Parse the video to extract the temporal state of all nodes. Load `/app/edges.csv` and your parsed video data into a SQLite database at `/home/user/network.db`. Use optimized schema design (e.g., proper indexes) so queries are highly performant. 
2. **Graph Routing Script:** Write a Python script at `/home/user/router.py` that calculates the lowest-cost path between two nodes at a specific time `T`. 
   - The script must read from the SQLite database to identify which nodes are online at time `T`. An offline node cannot be traversed, used as a source, or used as a destination.
   - Use parameterized SQL queries to safely fetch the valid edges or neighbors.
   - Implement a shortest-path algorithm (like Dijkstra's) in Python.

**Script Interface:**
Your script must be executable and accept exactly three positional integer arguments: `src`, `dst`, and `time_sec`.
```bash
python3 /home/user/router.py <src> <dst> <time_sec>
```

**Output Format:**
The script must print a single line to standard output:
- If a path exists: `PATH:<node_list> COST:<total_cost>` (e.g., `PATH:0,15,25,99 COST:42.5`)
- If the source or destination is offline, or if no path exists: `NO PATH`

Your implementation will be exhaustively fuzzed against a reference implementation with random inputs. Ensure your script is highly efficient (e.g., by pre-processing the video into the database rather than analyzing the MP4 on every invocation). Do not use external graph libraries like `networkx`; implement the traversal and SQL integration yourself.