I am a researcher organizing a large collection of datasets. My automated workflow orchestrator is frequently deadlocking, and I suspect it's because there are cyclic dependencies in my dataset lineage graph. 

I need you to write a C++ program that reads the dataset relationships, maps them into an in-memory directed graph, and detects all the cycles. 

Here are the specific requirements:
1. Fetch the `nlohmann/json` single-header library to parse JSON. You can download it to `/home/user/json.hpp` using:
   `wget https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp`
2. I have a file located at `/home/user/lineage.json` which contains a JSON array of dependency objects mapping a source dataset to a target dataset (e.g., `{"source": "dataset_A", "target": "dataset_B"}`).
3. Write a C++ program at `/home/user/find_cycles.cpp` that includes `json.hpp`, reads `/home/user/lineage.json`, and builds a directed graph.
4. Implement an algorithm (like Tarjan's or Kosaraju's, or a simple DFS) to find all Strongly Connected Components (SCCs) in the graph. Filter out any components that have fewer than 2 nodes (since self-loops don't exist in my dataset, and single nodes aren't cycles).
5. The program must output a JSON file at `/home/user/cycles_output.json` conforming to this exact schema:
   ```json
   {
     "cycles": [
       ["node1", "node2"],
       ["node3", "node4", "node5"]
     ]
   }
   ```
   **Sorting rules to ensure strict determinism:** 
   - Within each cycle array, the node IDs *must* be sorted alphabetically.
   - The outer `cycles` array *must* be sorted alphabetically by the first element of each inner array.
6. Compile your program using `g++ -std=c++17 /home/user/find_cycles.cpp -o /home/user/find_cycles` and run it.

Please write, compile, and execute the code to generate `/home/user/cycles_output.json`.