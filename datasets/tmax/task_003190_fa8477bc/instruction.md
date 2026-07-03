You are assisting a data researcher in building a strict validation pipeline for an academic dataset tracking system. The researcher ingests thousands of experiment log files (in JSON format) and needs a programmatic filter to separate genuine records from fraudulent or malformed ones. 

The dataset logs define relationships between variables, represented as a graph. You must build a Rust CLI tool that validates these logs against a canonical dataset schema.

Here is your workflow:

1. **Fix the Vendored Library**: 
   The researcher relies on a local, vendored Rust library called `dataset_graph` located at `/app/vendored/dataset_graph`. However, the library is currently broken due to a deliberate configuration perturbation made during a recent migration (it fails to compile). You must diagnose and fix this package so it builds successfully.

2. **Create the Validator Tool**:
   Initialize a new Rust binary project at `/home/user/dataset_filter`. Add the fixed local `/app/vendored/dataset_graph` as a dependency.
   
3. **Implement the Filter Logic**:
   Your Rust CLI must take exactly two arguments: a path to the canonical graph schema JSON, and a path to an experiment log JSON.
   Usage: `cargo run -- <graph_schema.json> <log.json>`

   The canonical graph schema at `/app/graph_schema.json` is a simple adjacency list:
   ```json
   {
     "nodes": ["A", "B", "C", "D", "E"],
     "edges": [["A", "B"], ["B", "C"], ["C", "D"]]
   }
   ```

   The experiment log JSON looks like this:
   ```json
   {
     "experiment_id": "EXP-1234",
     "timestamp": "2023-10-01T12:00:00Z",
     "source_node": "A",
     "target_node": "D",
     "metrics": {}
   }
   ```

   **Validation Rules (The resulting binary must exit with code 1 if ANY rule fails, and code 0 if ALL pass):**
   * **Rule 1:** The JSON must contain `experiment_id`, `timestamp`, `source_node`, and `target_node`.
   * **Rule 2:** The `timestamp` year must be 2024 or earlier.
   * **Rule 3:** You must parse the `graph_schema.json` using the `dataset_graph::Graph::from_json` function, and then use the library's `shortest_path(source, target)` method. 
   * **Rule 4:** If no path exists between `source_node` and `target_node`, OR if the shortest path distance is strictly greater than 3 edges, the log is deemed fraudulent.

4. **Integration**:
   Ensure your binary is compiled and works perfectly as a filter. We will test it against a hidden corpus of clean and evil JSON files. Clean files must return exit code 0. Evil files must return exit code 1.