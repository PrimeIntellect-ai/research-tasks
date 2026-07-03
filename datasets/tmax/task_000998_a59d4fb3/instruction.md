You are a data analyst tasked with analyzing a regional logistics network. You have been provided with two poorly documented CSV files in your home directory: `/home/user/stations.csv` and `/home/user/routes.csv`.

Your objective is to reverse-engineer the data model, load the data into a relational database, optimize it, and find the fastest route between two specific stations.

Here are your specific instructions:

1. **Reverse Engineer the Data Model**: 
   Examine the two CSV files. Figure out how they relate to each other. One file contains station information, and the other contains route connections (edges) between stations, including the transit time (cost) and the operational status of the route. Note that some routes may be inactive and must NOT be used.

2. **Database Construction & Index Strategy**:
   Write a Python script at `/home/user/setup_db.py` that reads the CSVs and loads them into a new SQLite database located at `/home/user/network.db`.
   Alongside this, you must write a pure SQL file at `/home/user/schema.sql` containing the `CREATE TABLE` and `CREATE INDEX` statements you used. You must design and include at least two indexes in `schema.sql` that specifically optimize querying outgoing and incoming active routes for a given station.

3. **Shortest Path Computation**:
   Write a Python script at `/home/user/shortest_path.py` that connects to `/home/user/network.db` and computes the shortest path (minimum total transit time) from the station named "Alpha Hub" to the station named "Omega Terminus". You may use standard Python libraries or install external ones like `networkx` if you prefer.

4. **Output Verification**:
   Your `shortest_path.py` script must output the final result to a text file at `/home/user/solution.txt`.
   The file must contain exactly two lines:
   - Line 1: The total transit time (an integer).
   - Line 2: The comma-separated list of station IDs representing the path, starting with Alpha Hub's ID and ending with Omega Terminus's ID.

Example `solution.txt` format:
45
8,15,22,4

Ensure all your scripts are executable or can be run via `python3 <script>`. Leave the final `network.db`, `schema.sql`, and `solution.txt` in the `/home/user` directory.