You are a Database Reliability Engineer (DBRE) tasked with replacing a legacy, proprietary backup routing calculator with a modern Python implementation. 

Our global database infrastructure stores backups across various regional storage nodes. When a database cluster fails, we must route the backup files through our network to the target recovery datacenter. We currently use a compiled, closed-source binary located at `/app/route_calc` to determine the optimal recovery path.

We need to deprecate this binary, but its logic is undocumented. Your task is to reverse-engineer its routing behavior and write a Python script that produces **bit-exact equivalent output** for any given network topology.

**System Details:**
1. The binary `/app/route_calc` takes two arguments:
   `> /app/route_calc <network_topology.json> <target_node_id>`
2. The `network_topology.json` contains a graph of datacenters (nodes) and network links (edges). 
   - Nodes have an `id` (string) and a boolean `is_backup_storage`.
   - Edges have a `src` (string), `dst` (string), `latency_ms` (int), and `throughput_penalty` (int).
3. The binary outputs a JSON array of strings representing the ordered sequence of node IDs in the optimal path from ANY `is_backup_storage` node to the `<target_node_id>`.

**Your Objective:**
1. Analyze the binary `/app/route_calc` to understand exactly how it calculates the "optimal" path (how it weighs edges, how it handles multiple storage nodes, and how it breaks ties).
2. Write a Python script at `/home/user/route_calc.py` that takes the exact same command-line arguments and prints the exact same JSON array to standard output.
3. Your script must be robust enough to handle any valid topology JSON and output identical results to the proprietary binary.

**Execution Format:**
Your script will be invoked by our automated systems exactly like this:
`python3 /home/user/route_calc.py <topology.json> <target_node_id>`

You may use standard Python libraries or install packages like `networkx` to help with graph traversal and shortest path computation.