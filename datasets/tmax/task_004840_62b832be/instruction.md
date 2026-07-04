You are a data engineer building a robust ETL pipeline for processing and projecting organizational hierarchy graphs. We frequently receive batched graph data (nodes and directed edges) from various internal systems. However, some of this data is malformed—containing cyclic dependencies or excessively deep hierarchies—which causes our downstream recursive SQL queries to fail.

Your task consists of two parts:

**Part 1: Audio Extraction**
We have an audio recording of a stakeholder meeting outlining the initial configuration for our graph materialized views. 
1. Use an appropriate tool (like `whisper` or similar speech-to-text pipeline, which you may need to install) to transcribe the audio file located at `/app/meeting.wav`.
2. Extract the name of the root node and the baseline score mentioned in the audio.
3. Save this information in `/home/user/root_info.txt` in exactly this format:
`Root: <NodeName>, Score: <Number>`

**Part 2: Adversarial Graph Filter**
You must write a Python script `/home/user/graph_filter.py` that acts as a sanitizer for incoming graph data. 
The script must take an input directory and an output directory as arguments:
`python3 /home/user/graph_filter.py <input_dir> <output_dir>`

The `<input_dir>` will contain multiple JSON files. Each file contains a list of directed edges representing a graph, formatted as follows:
`[{"source": "NodeA", "target": "NodeB"}, {"source": "NodeB", "target": "NodeC"}]`

Your script must analyze each graph and enforce the following rules:
- **No Cycles:** The graph must be a Directed Acyclic Graph (DAG). If any cycle is detected, the graph is invalid.
- **Max Depth Limit:** The longest path in the graph must not exceed 10 edges. If the hierarchical depth is greater than 10, the graph is invalid.

For every file in the `<input_dir>`:
- If the graph violates any of the above rules, it is considered "evil" and must be completely ignored (rejected).
- If the graph passes all rules ("clean"), the file should be copied to the `<output_dir>` unmodified.

Ensure your Python script relies on robust graph analytics logic (e.g., topological sorting, recursive DFS for cycle detection and longest path). You may install and use libraries like `networkx` if desired.