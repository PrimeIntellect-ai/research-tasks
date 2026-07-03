You are a data analyst investigating financial transaction records. We have exported relational data into two CSV files: `/home/user/nodes.csv` and `/home/user/edges.csv`. These represent a knowledge graph of entities and transactions.

Your task is to write and execute a C++ program that reads these CSV files, maps them into an efficient in-memory indexed graph structure, and performs a pattern matching query to detect potential cyclical money laundering patterns.

Here are the file formats:
`/home/user/nodes.csv`
```csv
node_id,node_type,name
```

`/home/user/edges.csv`
```csv
src_id,dst_id,rel_type,amount
```

You need to find all valid "3-cycles" (triangles) in the graph that match the following pattern:
1. Entity A transfers to Entity B.
2. Entity B transfers to Entity C.
3. Entity C transfers to Entity A.
4. For all three edges in the cycle, the `rel_type` MUST exactly equal "TRANSFER".
5. For all three edges in the cycle, the `amount` MUST be strictly greater than or equal to `1000`.

Requirements:
1. Write a C++ program (e.g., in `/home/user/analyzer.cpp`) to solve this. Compile it using `g++` (C++17 is available).
2. The program must implement an efficient index strategy (like an adjacency list utilizing hash maps) to ensure the graph can be queried efficiently, as doing full O(N^3) tabular scans on the edges would be too slow in a real scenario.
3. The program should output the detected cycles to a text file located at `/home/user/cycles.txt`.
4. Formatting rules for `/home/user/cycles.txt`:
   - Each line should represent exactly one detected 3-cycle.
   - For each cycle, print the three `node_id` strings separated by commas, with NO spaces.
   - To ensure a deterministic output, the three IDs on a given line MUST be sorted in ascending lexicographical (alphabetical) order, regardless of the flow direction in the cycle. (e.g., if the cycle is 999 -> 100 -> 500 -> 999, the line must be `100,500,999`).
   - The lines in the file must also be sorted in ascending lexicographical order.
   - Each unique cycle should only be printed once.

Create your C++ script, compile it, run it against the CSVs, and ensure `/home/user/cycles.txt` is produced exactly as specified.