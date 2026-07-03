You are tasked with extracting network topology data embedded in a video stream, constructing a relational database, and writing a highly optimized recursive query to analyze the network's hierarchy. 

A monitoring system has encoded network link formations into a video file located at `/app/network_feed.mp4`. 

Step 1: Data Extraction
Using Python (and tools like `ffmpeg` or `opencv-python`), analyze the frames of `/app/network_feed.mp4`. 
For every frame (0-indexed), check the exact center pixel `(width // 2, height // 2)`. If the Red channel value of this pixel is greater than 200 (in RGB format), an edge is formed. 
For each detected frame index `f`, the edge is defined as:
- `parent_node` = `(f * 7) % 100`
- `child_node` = `f`

Step 2: Database Construction
Create an SQLite database at `/home/user/network.db`.
Create a table named `topology` with columns `parent_node` (INTEGER) and `child_node` (INTEGER).
Insert all extracted edges into this table. Ensure there are appropriate indexes for query optimization.

Step 3: Query Optimization
We need to calculate the maximum depth of every node in the graph, starting from the root nodes. A root node is defined as any `parent_node` that never appears as a `child_node`. 
Write a highly optimized SQL query using a Recursive Common Table Expression (CTE) to compute the depth of each node. The root nodes have a depth of 0. 
Save your SQL query in a file exactly at `/home/user/analyze_hierarchy.sql`. 
The query must output two columns: `node_id` and `max_depth`, sorted by `node_id` ascending.

The execution speed and accuracy of your query will be rigorously tested against a massive mock database using your saved SQL file. You must ensure your CTE handles potential performance bottlenecks (like evaluating duplicate paths) and that your database schema includes indexes that optimize this recursive lookup.