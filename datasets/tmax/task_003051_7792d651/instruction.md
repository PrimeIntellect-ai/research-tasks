You are a data analyst tasked with analyzing an enterprise communication network to identify information bottlenecks. 

You have been given two headerless CSV files in `/home/user/data/`:
1. `graph_x.csv`
2. `graph_y.csv`

Through data model reverse engineering, you must determine which file represents the graph's nodes and which represents the directed edges. 
- The **nodes** dataset contains three columns: `ID` (integer), `Role` (string), and `Department` (string).
- The **edges** dataset contains three columns representing communications: `Sender ID` (integer), `Receiver ID` (integer), and `Timestamp` (integer, epoch seconds). You will need to infer the exact column order based on the data types and logical relations (IDs in the edge table will map to IDs in the node table).

Your objective is to perform a specific graph analytics query by chaining together a pipeline that extracts a particular knowledge graph pattern:
Find all communication paths of length 2 where an **'Engineer'** messages a **'Manager'**, and that *same* **'Manager'** messages a **'Director'**. 
The second message (Manager -> Director) must occur strictly *after* the first message (Engineer -> Manager), but within exactly one hour (i.e., `0 < timestamp2 - timestamp1 <= 3600`).

Once you have identified all such valid paths, calculate a localized "betweenness" metric for the Managers: count how many of these specific valid paths each Manager acts as the middleman for.

Finally, extract the top 3 Managers with the highest path counts. If there is a tie in the count, sort the tied records by Manager ID in ascending order.

Write your final output to `/home/user/influencers.csv`. The file should contain exactly three lines (no headers), formatted exactly as:
`ManagerID,PathCount`