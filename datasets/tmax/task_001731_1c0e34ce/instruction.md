You are a data engineer building an ETL pipeline for a graph-based network monitoring system. You have been given raw video footage of a network simulation, alongside a dataset of historical network graph snapshots. 

Your task is divided into three parts:

**Part 1: Video Artifact Extraction**
There is a video file located at `/app/network_simulation.mp4`. This video encodes network failure events. 
1. Use `ffmpeg` to extract the exact number of keyframes (I-frames) from this video. 
2. Save this count to `/home/user/keyframe_count.txt`. This integer represents the global "failure severity multiplier" for the day.

**Part 2: Adversarial Graph Filtering**
You have historical network graph snapshots in JSON format located in two directories: `/app/corpora/clean/` and `/app/corpora/evil/` (for testing your script). 
You must write a Bash script at `/home/user/sanitize_graphs.sh` with the following signature:
`./sanitize_graphs.sh <input_dir> <output_dir>`

This script must process all `.json` files in the `<input_dir>`. It must copy the file to `<output_dir>` ONLY IF the graph is "clean". A graph is considered "evil" (and must be rejected/ignored) if it violates ANY of the following rules:
- The JSON is malformed.
- Any node `id` contains characters other than alphanumeric, hyphens, or underscores (`[A-Za-z0-9_-]`).
- Any edge `weight` is a negative number.
- Any node has the property `"indexed": true` but is missing the `"idx_key"` property.
Use `jq` and native bash utilities for this.

**Part 3: Cross-Representation Mapping**
Once you have verified your script, run it against a staging directory (assume the pipeline will do this automatically later). For now, take a sample clean graph (you can create a dummy one based on the clean rules) containing at least 3 nodes and 2 edges, and write a script `/home/user/convert.sh <input.json>` that converts the valid JSON graph into three formats:
1. `/home/user/export_relational.csv`: A relational table of edges (headers: `source,target,weight`).
2. `/home/user/export_document.jsonl`: A JSON-lines file where each line is a document representing a node and an array of its outgoing edges.
3. `/home/user/export_graph.dot`: A valid DOT format graph for Graphviz visualization.

Ensure your scripts are executable.