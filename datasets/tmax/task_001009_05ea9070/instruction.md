You are assisting a compliance officer in auditing physical access controls. The company's floor plan has been updated, and the only record of the new security zone topology is an automated backup video from the topology mapping software.

Your task is to reconstruct the floor plan graph, optimize it for querying, and write a pathfinding tool to help the compliance officer audit potential unauthorized movement paths.

**Step 1: Extract Topology from Video**
You have been provided with a video file at `/app/cctv_topology.mp4`. 
The video is exactly 15 seconds long. Every exactly 1.0 second (starting at 0.0), the video flashes a single line of text on a white background representing a bidirectional door connection between two security zones. 
The text format is: `ZONE_A <-> ZONE_B`.
Extract all unique connections from the video (you may use `ffmpeg` and `tesseract-ocr`, which you can install if needed).

**Step 2: Database Construction & Optimization**
Create an SQLite database at `/home/user/audit.db`.
Create a table named `doors` with the schema: `CREATE TABLE doors (zone1 TEXT, zone2 TEXT);`
Insert all extracted connections into this table. Since the doors are bidirectional, ensure your data representation allows traversing from `zone1` to `zone2` and vice versa.
To optimize graph traversal queries, create appropriate indexes on the `doors` table. 

**Step 3: Path Auditor Script**
Write a Python script at `/home/user/path_check.py` that calculates the shortest path between any two zones using the database you just created. 
The script must:
- Be executable from the command line.
- Accept exactly two arguments: the starting zone and the target zone. Example: `python3 /home/user/path_check.py ZONE_ALPHA ZONE_OMEGA`
- Query the `/home/user/audit.db` database. You must use a Recursive CTE (Common Table Expression) in your SQL query to find the shortest path, or implement a graph traversal algorithm in Python that queries the database.
- Print the shortest path as a comma-separated list of zones, starting with the source and ending with the target. Example output: `ZONE_ALPHA,ZONE_BETA,ZONE_OMEGA`
- If multiple shortest paths of the same length exist, you may return any of them (the verifier will check the path length and validity). If no path exists, print exactly `NO_PATH`.

Make sure your Python script strictly outputs ONLY the resulting string to standard output, with no additional logging, as it will be heavily tested via automated fuzzing against an oracle.