You are a data analyst working with a dataset exported from an old system. The data represents a knowledge graph but has been flattened into two relational CSV files: `/home/user/nodes.csv` and `/home/user/edges.csv`.

Your task is to write a Go program (`/home/user/analyze_graph.go`) that reads these files, reconstructs the graph in memory, and finds a specific pattern. 

**Data Structure:**
1. `/home/user/nodes.csv` has the header: `id,type,name`
   - `id`: Unique string identifier
   - `type`: The type of the node (e.g., "Person", "Company", "Industry")
   - `name`: The display name of the entity
2. `/home/user/edges.csv` has the header: `source,target,relation`
   - `source`: ID of the source node
   - `target`: ID of the target node
   - `relation`: The type of relationship (e.g., "WORKS_FOR", "OPERATES_IN")

**Pattern to Match:**
Find all instances where a `Person` node has a `WORKS_FOR` relationship to a `Company` node, and that same `Company` node has an `OPERATES_IN` relationship to an `Industry` node whose name is exactly `"AI"`.

**Requirements:**
1. Write the logic entirely in Go.
2. The Go program must output the results as a JSON array to `/home/user/matches.json`.
3. Each object in the JSON array must represent one matched path and contain exactly these keys: `person`, `company`, `industry`. The values should be the `name` attributes of the respective nodes.
4. The JSON array must be sorted alphabetically by the `person`'s name.
5. Format the JSON with 2-space indentation.
6. Compile and run your Go program to generate the final `matches.json` file.