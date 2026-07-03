You are a data analyst tasked with analyzing an internal corporate communication network. You have been provided with two CSV files containing communication data. 

Your objective is to write a Go program that materializes this data into an in-memory directed graph, performs graph analytics, and executes pattern matching to find specific communication structures.

The data files are located at:
1. `/home/user/employees.csv` - Contains employee metadata.
   Format: `id,name,department`
2. `/home/user/emails.csv` - Contains communication logs.
   Format: `sender_id,receiver_id,timestamp`

Write a Go program at `/home/user/analyze_graph.go` that does the following:
1. **Graph Materialization**: Build a directed, unweighted graph where nodes are employees and edges represent email communication (an edge exists from A to B if A emailed B at least once). Ignore duplicate edges between the same sender and receiver.
2. **Centrality Analysis**: Identify the employee `id` with the highest Out-Degree centrality (the person who emailed the highest number of unique employees). If there is a tie, pick the one with the lowest numeric `id`.
3. **Pattern Matching (Triangles)**: Find the total number of unique closed triad patterns (triangles) where A emails B, B emails C, and C emails A. **Constraint:** All three employees in the triangle must belong to the *same department*. (Note: A triangle is defined by the unique set of 3 nodes {A, B, C}. Do not count permutations of the same 3 nodes as multiple triangles).

Once your Go program calculates these metrics, it must write the results to a file named `/home/user/graph_results.txt` exactly in the following format:

```
Highest Out-Degree: [ID]
Same-Department Triangles: [COUNT]
```

Replace `[ID]` and `[COUNT]` with your calculated integer values.