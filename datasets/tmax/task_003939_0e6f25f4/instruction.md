You are a data analyst taking over a project from a colleague. They were trying to analyze internal communication networks to find the shortest influence path between the CEO and a newly hired engineer. However, their bash/awk pipeline resulted in an implicit cross-join (Cartesian product) of the dataset, which crashed the server due to OOM errors.

Your task is to correctly perform this analysis using a graph-based approach.

You have two files located in your home directory:
1. `/home/user/employees.csv` - Contains employee metadata: `emp_id,name,department`
2. `/home/user/communications.csv` - Contains communication logs: `sender_id,receiver_id,message_count`

Treat the communication network as an **undirected graph** (an edge exists between A and B if A sent a message to B OR B sent a message to A. Ignore edge weights/message_count, multiple messages between the same pair just count as a single undirected edge). 

Here is what you need to do:
1. Parse the CSV files to build the communication graph.
2. Find the **shortest path** between `E001` and `E012`. (The graph is designed so there is only one unique shortest path).
3. For **each employee in that shortest path**, calculate their **degree centrality** within the *entire* network. (Degree centrality here is defined simply as the total number of unique employees they are connected to).
4. Export the results to a JSON file at `/home/user/path_analysis.json`.

The output file `/home/user/path_analysis.json` MUST exactly match this format:
```json
{
  "shortest_path": ["E001", "...", "E012"],
  "centrality": {
    "E001": 2,
    "ID2": X,
    "ID3": Y,
    "E012": 1
  }
}
```

You may use any programming language available in the standard environment (Python 3 is recommended) to write your script. Make sure your script handles the data efficiently and outputs the correct JSON structure.