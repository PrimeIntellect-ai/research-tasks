You are a database administrator tasked with optimizing the refresh pipeline of a complex data warehouse. The warehouse has hundreds of materialized views, tables, and stored procedures with intricate dependencies. The current refresh strategy is inefficient, and you need to build a custom C++ query engine to analyze these dependencies and optimize the execution plan.

Your task is to write a C++ program that analyzes a dependency graph to find the most critical schema objects (graph centrality) and maps the execution path between specific objects (graph traversal).

**Step 1: The Data**
You will find a space-separated edge list of dependencies at `/home/user/schema_deps.txt`. 
Each line contains two strings representing schema objects: `ObjectA ObjectB`.
This means **ObjectA depends on ObjectB** (directed edge from ObjectA to ObjectB).

**Step 2: The C++ Tool**
Write a C++17 program at `/home/user/graph_optimizer.cpp`. It must:
1. Accept three command-line arguments: `<input_file> <source_node> <target_node>`.
2. Parse the dependency graph.
3. **Graph Analytics (Centrality):** Calculate the "dependency centrality" of all nodes, defined simply as the **in-degree** of the node when considering edges as `Dependant -> Dependency`. In other words, count how many objects directly depend on each object. Resolve ties alphabetically by object name.
4. **Graph Traversal (Shortest Path):** Find the shortest dependency path from `<source_node>` to `<target_node>` using BFS.
5. Output the results as a strictly formatted JSON to standard output.

**Step 3: Compilation and Execution**
1. Compile your code: `g++ -O3 -std=c++17 /home/user/graph_optimizer.cpp -o /home/user/graph_optimizer`
2. Run your tool to analyze the path from `monthly_sales_report` to `raw_transactions`:
   `./graph_optimizer /home/user/schema_deps.txt monthly_sales_report raw_transactions > /home/user/optimization_report.json`

**Expected JSON Format for `/home/user/optimization_report.json`:**
```json
{
  "top_dependencies": [
    "node_with_highest_in_degree",
    "node_with_second_highest",
    "node_with_third_highest"
  ],
  "shortest_path": [
    "monthly_sales_report",
    "intermediate_view_1",
    "raw_transactions"
  ]
}
```
*Note: `top_dependencies` must contain exactly the top 3 most depended-upon objects. The `shortest_path` must be an array of strings representing the path sequence. Format the JSON exactly as shown above (standard spacing/indentation).*