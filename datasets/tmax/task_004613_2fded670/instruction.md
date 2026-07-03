You are acting as a compliance officer auditing financial systems for illicit money flows. We have a set of transaction networks represented as directed graphs in JSON (node-link format). Your objective is to fix our internal graph analysis library, write a detection script, and flag networks that violate compliance rules.

A compliance violation occurs if there is a **directed path of length 3 or less** from any node with the attribute `status="sanctioned"` to any node with the attribute `status="cleared"`. (Path length is the number of edges. E.g., Sanctioned -> A -> B -> Cleared has length 3).

**Step 1: Fix the Vendored Package**
We vendor a specific version of `networkx` at `/app/networkx-vendored`. However, an intern accidentally broke the `setup.py` file, preventing installation. 
1. Identify and fix the syntax error in `/app/networkx-vendored/setup.py`.
2. Install the package into your Python environment (`pip install -e /app/networkx-vendored`).

**Step 2: Write the Detector**
Create a Python script at `/home/user/detect_violations.py` with the following CLI signature:
`python /home/user/detect_violations.py <input_directory> <output_file>`

- The `<input_directory>` will contain several JSON files, each representing a single directed graph in NetworkX node-link format.
- Your script must load each JSON graph, project it into a directed graph, and compute the shortest paths to check for compliance violations.
- If a graph contains at least one compliance violation (a directed path $\le 3$ edges from a 'sanctioned' node to a 'cleared' node), its filename (just the basename, e.g., `graph_05.json`) must be written to the `<output_file>`, one per line.
- If a graph is compliant (no such path, or all paths from 'sanctioned' to 'cleared' are strictly greater than 3 edges), do not write its filename to the output file.

**Step 3: Verification**
To prove your solution works, run your script on the provided training corpus (though the automated test will use a hidden evaluation corpus of identical format).
You can test your script against the data in `/app/corpus/evil/` (all of which are violations) and `/app/corpus/clean/` (all of which are compliant). 

Ensure your script operates entirely offline and strictly relies on the vendored package.