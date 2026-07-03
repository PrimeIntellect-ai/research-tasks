You are helping a researcher organize a complex set of dataset dependencies. The researcher has simulated the evolution of this data network, and the simulation is recorded in a video file located at `/app/topology_sim.mp4`.

First, you need to determine the total number of frames in the video `/app/topology_sim.mp4`. Let this number be `F`. You may use `ffmpeg` or `ffprobe`.

Second, write a Python script at `/home/user/path_finder.py` that acts as a query engine for the dataset graph. The script must accept exactly two command-line arguments:
1. `--graph`: A JSON string representing a directed graph (e.g., `'{"1": [2, 3], "2": [4], "3": [], "4": []}'`). Keys are string node IDs, and values are lists of adjacent string node IDs.
2. `--start`: A string representing the starting node ID.

Your script must:
1. Parse the JSON graph.
2. Compute the shortest path distance (number of edges) from the `start` node to all other reachable nodes. The distance to the `start` node itself is 0.
3. Filter out any nodes where the shortest path distance is STRICTLY GREATER THAN `(F % 10)`. (Substitute the actual value of `F` you found into your code or read it dynamically, but it must reflect the frame count of the video).
4. For the remaining reachable nodes, sort them first by their distance in DESCENDING order, and then by their node ID in ASCENDING order.
5. Print the sorted node IDs as a single comma-separated string to standard output (e.g., `4,2,3,1`). Do not print any other text.

The researcher's automated test suite will rigorously test your `/home/user/path_finder.py` script against thousands of random graphs to ensure it perfectly matches the expected logic (bit-exact output equivalence). Ensure your script handles cases where nodes have no outgoing edges or the start node cannot reach certain parts of the graph.