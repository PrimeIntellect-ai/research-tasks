You are a data analyst working with a massive dataset of hierarchical CSV files representing a global supply chain network. You are using a proprietary internal tool called `csv_graph_mapper` (located in `/app/csv_graph_mapper`) to map this relational CSV data into a graph structure for hierarchical analysis.

However, the internal tool is currently broken. Whenever you try to load the CSV files using its concurrent ingestion feature, the underlying database encounters constant deadlocks and the performance grinds to a halt (taking several minutes for even small files). 

Your task consists of the following steps:
1. **Fix the Tool**: Inspect the `csv_graph_mapper` Python package in `/app/csv_graph_mapper` and resolve the deadlock and performance issues in its ingestion logic. You will need to modify its source code.
2. **Build the Ingestion Script**: Write a script at `/home/user/analyze_supply_chain.py` that imports `csv_graph_mapper`. Your script should initialize the graph database, configure the appropriate indexing strategy for the `part_id` column, and concurrently load `/home/user/data/components.csv` (nodes) and `/home/user/data/dependencies.csv` (edges).
3. **Execute a Hierarchical Query**: Using the package's query interface (which supports SQLite CTEs for recursive traversal), write a recursive query to find the "maximum dependency depth" of the entire supply chain graph.
4. **Output the Results**: Save the results in `/home/user/output.json` conforming exactly to this schema:
   ```json
   {
       "max_depth": 14,
       "total_nodes": 50000,
       "total_edges": 49999
   }
   ```

Requirements:
- Your final script (`/home/user/analyze_supply_chain.py`) must run from start to finish in **under 3.0 seconds**. The unmodified vendored package will fail or take over 60 seconds.
- You must validate your graph output structure before writing the JSON file.