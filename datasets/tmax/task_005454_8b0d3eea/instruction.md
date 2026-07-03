You are a data engineer building an ETL pipeline for our automated warehouse tracking system. 

We have a video artefact of a delivery robot moving through our warehouse floor at `/app/robot_tracking.mp4`. The video captures the robot passing by specific numbered waypoint markers (black text on white background) at each intersection it visits. 

Additionally, you have access to a SQLite database at `/app/warehouse.db`. However, the documentation for this database was lost. You need to reverse engineer its schema to understand how the warehouse graph (nodes, edges, and distances) is stored.

Your task is to build a Python ETL script at `/home/user/pipeline.py` that does the following:
1. Extracts the sequence of waypoints the robot visited from the video. You will need to process the video (using `ffmpeg` and Python tools like `opencv-python` and `pytesseract` which you can install) to read the waypoint IDs as the robot passes them. Filter out noise to get the ordered list of unique visited waypoints (e.g., if the robot sees '5' for several frames, it counts as one visit to waypoint 5).
2. Reverse engineers the `warehouse.db` schema to find how the graph topology and edge weights (distances) are represented.
3. Constructs parameterized queries to retrieve the total distance of the *actual path* the robot took based on the video sequence.
4. Implements a graph traversal algorithm to compute the *optimal (shortest) path* distance between the robot's starting waypoint and its final destination waypoint.
5. Prints a single floating-point number to standard output representing the "Path Efficiency Metric", defined as: `optimal_path_distance / actual_path_distance`.

Your script must run autonomously without user interaction when executed via `python3 /home/user/pipeline.py`. Ensure your extraction handles duplicate detections correctly (a waypoint is considered left when a different waypoint is detected or the video ends).

The automated verifier will run your script and compare your output to the ground-truth efficiency metric. Your answer must be within 0.05 of the correct ratio.