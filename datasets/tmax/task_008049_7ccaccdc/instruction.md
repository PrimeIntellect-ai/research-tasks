You are acting as an assistant to a computational chemist running molecular network simulations. To prepare for a parallel simulation, we need to perform a simple spatial domain decomposition on our molecular graph.

A molecular graph is provided in `/home/user/molecule_graph.txt`. The file format is as follows:
- The first line contains `NODES N`, where N is the number of atoms.
- The next N lines contain the node data: `ID X Y Z` (integer ID, followed by three floating-point coordinates).
- Following the nodes, there is a line `EDGES M`, where M is the number of bonds.
- The next M lines contain the edges, each represented by two node IDs: `ID1 ID2`.

Your task is to write a C program located at `/home/user/decompose.c` that parses this file and performs the following operations:

1. **Domain Decomposition**: Assign each node to one of two domains based on its X-coordinate.
   - Domain 0: X < 0.0
   - Domain 1: X >= 0.0

2. **Analysis**:
   - Count the total number of "cross-domain edges". A cross-domain edge is a bond where one node is in Domain 0 and the other is in Domain 1.
   - Find the node belonging to Domain 0 that has the highest degree (most connected edges overall). If there is a tie, select the one with the smallest ID.

3. **Visualization**:
   - Generate an ASCII bar chart representing the number of nodes in each domain. Save this exactly to `/home/user/visualization.txt`.
   - The format must be `Domain X: [stars]`, where there is one `*` (asterisk) for every 2 nodes in that domain (rounded down).
   Example format:
   ```
   Domain 0: **
   Domain 1: ***
   ```

4. **Summary Report**:
   - Write a summary of the analysis to `/home/user/decomposition_summary.log`.
   - The log file must contain exactly these two lines (with the correct computed integers):
   ```
   Cross-domain edges: <count>
   Max degree node in domain 0: <node_id>
   ```

Please write the C code, compile it to an executable named `/home/user/decompose`, and run it so that the output files are generated.