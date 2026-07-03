You are assisting a researcher who is organizing a complex, multi-format dataset of academic collaborations. The data is currently scattered across three different representations:
1. An SQLite database containing researcher metadata (Relational).
2. A CSV file containing collaboration links (Graph edges).
3. A JSON file containing publication topics for each researcher (Document).

Your task is to write a Go program that bridges these formats, calculates the shortest collaboration path between two researchers, and outputs the result in a strictly validated JSON format.

**Data Sources (Already existing on the system):**
*   **Relational:** An SQLite database located at `/home/user/data/researchers.db`. It has a table `nodes` with columns `id` (INTEGER) and `name` (TEXT).
*   **Graph:** A CSV file located at `/home/user/data/edges.csv` with a header `source,target`. Each row represents an undirected collaboration edge between two researcher IDs.
*   **Document:** A JSON file located at `/home/user/data/topics.json`. It is a single JSON object where keys are researcher IDs (as strings) and values are arrays of topic strings.

**Requirements for the Go Program:**
1.  **Location:** Create your Go program at `/home/user/workspace/pathfinder.go`. You can initialize a Go module in `/home/user/workspace`. 
2.  **Dependencies:** Use `github.com/mattn/go-sqlite3` for SQLite interaction.
3.  **Inputs:** The program should accept two command-line flags: `--source` (integer ID) and `--target` (integer ID).
4.  **Processing Steps:**
    *   Read the graph from `edges.csv` and compute the shortest path (in terms of number of edges) between the `--source` and `--target` IDs. If multiple paths have the same shortest length, any valid shortest path is acceptable.
    *   For each node in the computed path, query the SQLite database (`researchers.db`) to retrieve the researcher's `name`. **You must use parameterized queries** to prevent SQL injection, even though the inputs are internal.
    *   Retrieve the topics for each node from `topics.json`. If a node ID is missing from the JSON, default to an empty array `[]`.
5.  **Output:** The program must write the final path to a JSON file at `/home/user/output/path.json`.
    *   The output must strictly match this schema structure:
        ```json
        {
          "path": [
            {
              "id": 1,
              "name": "Alice",
              "topics": ["AI", "Graphs"]
            },
            ...
          ]
        }
        ```

Once the program is written, execute it with `--source 1` and `--target 5`. Ensure the final output file is generated correctly.