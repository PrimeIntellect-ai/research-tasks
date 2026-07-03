You are assisting a researcher in extracting and organizing a dataset from a combination of a video and a relational database.

You are provided with two artifacts:
1. A video file at `/app/experiment.mp4` which records a scientific instrument's indicator light. 
2. An SQLite database at `/app/graph.db` containing a large graph of experimental states. The database has a table `edges(source INTEGER, target INTEGER)`. The database is known to have some fragmented or unoptimized indexes.

Your task is to build a Rust application that performs the following workflow:
1. **Video Extraction**: Process `/app/experiment.mp4` to determine which frames are "active". A frame is considered "active" if its average grayscale pixel intensity is strictly greater than 100.0. (Treat the video as 0-indexed, meaning the first frame is frame 0).
2. **Database Querying**: The "active" frame numbers correspond exactly to node IDs in `/app/graph.db`. You must extract the induced subgraph of these active nodes (i.e., all edges from `edges` where BOTH `source` and `target` are in the set of active frame numbers).
3. **Graph Analytics**: Calculate the average clustering coefficient of this active subgraph. The clustering coefficient of a node is the number of edges between its neighbors divided by the maximum possible number of edges between its neighbors. The average clustering coefficient is the mean of the clustering coefficients of all nodes in the subgraph that have degree >= 2. (Nodes with degree < 2 do not contribute to the average).
4. **Optimization**: Ensure your database querying and extraction are reasonably optimized. 

Write the computed average clustering coefficient (as a standard decimal float) to `/home/user/result.txt`. 

Your primary implementation must be in Rust, using a Cargo project located at `/home/user/analyzer`. You may use system commands (like `ffmpeg`) to extract frames to a temporary directory if that makes your Rust implementation easier.

The automated test will evaluate the numerical value in `/home/user/result.txt`.