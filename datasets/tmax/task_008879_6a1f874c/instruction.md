You are a data analyst tasked with analyzing a communication network. You have been provided with two undocumented CSV files located at `/home/user/data/nodes.csv` and `/home/user/data/edges.csv`. 

The data engineering team exported these files without headers, and the columns are in an arbitrary order. 

Here is what you know about the data:
1. `nodes.csv` contains three columns: a person's Name (string), their Age (integer), and their unique User ID (integer).
2. `edges.csv` contains four columns representing communication events: a Unix Timestamp (integer), a Confidence Score (float), and two integer columns representing the User IDs of the two individuals communicating. 
3. The graph is **undirected**. Communication from A to B is the same as B to A.
4. There may be duplicate edges (multiple communications between the same pair) and self-loops (a user communicating with themselves).

Your objective is to reverse-engineer the data model by identifying which columns correspond to the User IDs, and then write a Rust program to process the graph and compute specific metrics.

Create a Rust project or standalone Rust script at `/home/user/graph_analyzer.rs` (if using a script, you can run it via `rustc` or set up a standard cargo project in `/home/user/graph_project`). The program must read the CSV files, build the network graph in memory, and calculate the following:
1. The **total number of unique, valid edges** (ignoring self-loops and treating multiple communications between the same two users as a single undirected edge).
2. The **Name of the person with the highest degree** (the highest number of unique connections to other people).
3. The **total number of unique triangles** in the graph (a triangle is a set of 3 distinct nodes where all three are mutually connected to each other).

Your Rust program must output the final results into a JSON file located at `/home/user/output.json` with the exact following structure:
```json
{
  "highest_degree_name": "NameHere",
  "total_edges": 0,
  "total_triangles": 0
}
```

You may use standard shell tools (awk, head, etc.) to inspect the files and test your assumptions before writing the Rust code. Do whatever is necessary to build, run, and successfully output the JSON file.