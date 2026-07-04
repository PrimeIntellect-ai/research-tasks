You are helping a researcher organize and extract dataset from a scientific video artifact.

We have a video file located at `/app/grid_flash.mp4`. This video represents a 5x5 sensor grid. Each sensor in the grid can either be "off" (black) or "on" (white). The video is 30 seconds long at 10 fps. 

Your task is to extract a weighted interaction graph from this video and store it in an optimized SQLite database, then export it.

**Rules for Graph Extraction:**
1. The video dimensions are 500x500 pixels. The grid is perfectly divided into 25 squares of 100x100 pixels each. 
2. Nodes are indexed 0 to 24 (row-major order, so top-left is 0, top-right is 4, bottom-right is 24).
3. A sensor is considered "on" in a frame if the average pixel intensity of the central 10x10 area of its square is > 128.
4. An interaction (edge) occurs between two **adjacent** nodes (horizontally or vertically) if they are both "on" in the exact same frame.
5. The weight of an edge is the total number of frames where both adjacent nodes were "on" simultaneously.

**Deliverables:**
1. Parse the video and extract the frame-by-frame data.
2. Build an SQLite database at `/home/user/sensor_graph.db`.
3. Create a table `edges (source INTEGER, target INTEGER, weight INTEGER)`. Ensure `source < target` for all rows, and only include edges with `weight > 0`.
4. Create an optimized index on the `weight` column.
5. Export the edges to a CSV file at `/home/user/edges_export.csv` with columns `source,target,weight` sorted by `weight` descending.

The automated verification will check your `edges_export.csv` against the ground truth edge weights using Mean Absolute Error (MAE). Your extraction needs to be highly accurate.