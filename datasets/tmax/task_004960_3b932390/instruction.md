You are a data engineer optimizing a highly concurrent ETL pipeline system that frequently experiences deadlocks. The system's monitoring dashboard has recorded the lock acquisition graph over the past hour, but the raw logs were lost. The only surviving record is a video export of the dashboard, which flashes a series of QR codes encoding the transaction dependency edges.

Your objective is to reconstruct the dependency graph, design a highly optimized database schema, and write a module to analyze the transactions for deadlocks and critical paths.

**Step 1: Data Extraction**
A video file is located at `/app/etl_monitor.mp4`. Throughout the video, QR codes are displayed. Extract the text from all unique QR codes in the video. 
Each decoded payload is a JSON string representing a directed dependency edge between two ETL jobs during a specific transaction:
`{"tx_id": <int>, "source": "<string>", "target": "<string>", "duration_ms": <int>}`
*(Hint: You can use `cv2` and `pyzbar` in Python to read the video frames and decode the QR codes.)*

**Step 2: Schema Design & Indexing**
Create a SQLite database at `/home/user/etl_graph.db`. 
Design a schema to store these dependency edges. You must design and create appropriate indexes to support extremely fast pathfinding and graph traversal on a per-`tx_id` basis. The performance of your schema and indexing strategy is critical.

**Step 3: Graph Analysis Implementation**
Write a Python script at `/home/user/analyze.py` that contains the following two functions. Do not execute the functions at the bottom of the script, just define them so they can be imported.

1. `def find_deadlocks(db_path: str) -> list[int]:`
   Analyzes the database and returns a deduplicated list of `tx_id`s (sorted in ascending order) that contain at least one cycle in their dependency graph (representing a transaction deadlock).

2. `def get_shortest_path_duration(db_path: str, tx_id: int, source: str, target: str) -> int:`
   Returns the minimum total `duration_ms` required to traverse from the `source` job to the `target` job for the given `tx_id`. If no path exists, return `-1`. Use parameterized SQL queries to prevent injection and maximize execution plan caching. You may use recursive CTEs or query the edges and compute in Python, but your method must be highly optimized.

**Evaluation Constraints:**
An automated verification script will import your `analyze.py` and benchmark your `get_shortest_path_duration` function by querying it 5,000 times with random parameters. 
Your success is determined by a **metric threshold**: The total time to execute the 5,000 queries must be **under 1.5 seconds**. If you fail to design the correct index strategy or use inefficient graph traversals, you will exceed this threshold.