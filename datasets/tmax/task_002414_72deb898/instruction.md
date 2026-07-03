You are a data analyst working on processing social network interaction logs. You have been provided with a CSV file containing directed interaction data between users. 

Your task is to write a C++ program that ingests this data into an SQLite database, performs advanced analytical and graph-like queries, and outputs the results to specific CSV files.

**Setup Instructions:**
1. A raw data file exists at `/home/user/network.csv` (you will need to assume it is there; do not modify it).
2. You may install necessary libraries. The C++ standard SQLite3 library will be useful (`libsqlite3-dev`).
3. Create your C++ program at `/home/user/process_network.cpp`.
4. Compile your program to `/home/user/process_network` and execute it to produce the outputs.

**Data Format (`/home/user/network.csv`):**
The CSV contains a header and four columns: `source,target,weight,timestamp`
- `source`: string (1 character)
- `target`: string (1 character)
- `weight`: integer
- `timestamp`: integer

**Requirements for the C++ Program:**
Your C++ program must use the SQLite3 API to create an in-memory database, load the data from `/home/user/network.csv`, and execute two distinct queries.

**Query 1: Analytical Aggregation (Window Functions)**
You need to identify the top interactions for each user.
- Calculate the `DENSE_RANK()` of each `target` for a given `source`, ordered by `weight` in descending order. If weights are equal, order by `timestamp` in ascending order.
- Filter the results to only include rows where the rank is 2 or better (i.e., rank <= 2).
- Write the results to `/home/user/window_results.csv`.
- The output CSV must not have a header.
- The format must be: `source,target,weight,rank`
- Sort the final output by `source` ascending, then `rank` ascending, then `target` ascending.

**Query 2: Graph Traversal (Recursive CTE)**
You need to analyze indirect connections by finding the strongest bottleneck paths of exactly length 2 starting from node 'A'.
- Use a Recursive CTE (Graph query pattern) to find all paths starting from `source` = 'A' that take *exactly* 2 steps (e.g., A -> B -> D).
- For each path, calculate the "bottleneck weight", which is the minimum `weight` along that specific path.
- If there are multiple length-2 paths to the same final destination, take the maximum of these bottleneck weights.
- Write the results to `/home/user/graph_results.csv`.
- The output CSV must not have a header.
- The format must be: `destination,max_bottleneck_weight`
- Sort the final output by `destination` ascending.

Ensure your C++ program gracefully handles the CSV reading, executes the SQL accurately, and writes the files precisely as requested.