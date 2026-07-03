You are an AI assistant helping a behavioral researcher organize and query experimental datasets. 

The researcher has an experiment where subjects navigate a network of locations. You need to build a C++ data querying service that integrates video logs, a relational database, and a graph document, exposing the unified data via an HTTP API.

Here are the components you have to work with:
1. **Video Log**: A video file at `/app/dataset_recording.mp4` containing the subject's navigation log. The video consists of a sequence of frames, where every exactly 2 seconds represents a distinct event. You need to use `ffmpeg` to extract these frames. The researcher has noted that the brightness of the center pixel (or average brightness of the frame) indicates the activity level for that 2-second epoch. 
2. **Graph Document**: A JSON file at `/app/graph.json` containing the adjacency list of the physical maze. It represents nodes and the distance (cost) between them.
3. **Relational DB**: An SQLite database at `/app/metadata.db` containing a table `subjects` (id, name) and an empty table `epochs` (subject_id, epoch_index, activity_level).

Your tasks are:
1. **Data Processing**: Extract the activity level from `/app/dataset_recording.mp4` for each 2-second epoch (e.g., epoch 0 is 0-2s, epoch 1 is 2-4s, etc.). Define activity level as the grayscale value (0-255) of the center pixel of the frame at the start of the epoch (0s, 2s, 4s...). Insert these records into the `epochs` table in `/app/metadata.db` for `subject_id = 1` using C++ parameterized SQL queries.
2. **Graph Querying**: Implement Dijkstra's algorithm in C++ to compute the shortest path between any two nodes defined in `/app/graph.json`.
3. **API Integration**: Create a C++ HTTP server listening on `127.0.0.1:8080`. You may use a lightweight header-only library like `cpp-httplib`.
   
The HTTP Server must expose these endpoints:
- `GET /path?start=<node_id>&end=<node_id>`: Returns a JSON object `{"path": ["A", "B", ...], "cost": 15}` representing the shortest path and its total cost.
- `GET /activity?epoch=<epoch_index>`: Queries the SQLite database using parameterized queries and returns `{"epoch": <index>, "activity": <level>}`.

Constraints:
- You must write the main service in **C++** (C++17 or later).
- You can use shell scripts or Python just for initial data extraction if necessary, but the HTTP API, graph traversal, and SQLite querying must be handled by the compiled C++ service.
- Run the C++ server in the background so it is actively listening on `127.0.0.1:8080` when you complete the task. Leave the server running.