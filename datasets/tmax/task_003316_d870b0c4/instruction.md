You are a web developer building a high-performance C backend component for a new REST API. This API is responsible for resolving task dependency graphs and returning execution orders. 

Your task consists of three parts: analyzing a legacy system mockup video, building the C-based graph resolver, and processing the mock data.

**Part 1: Video Analysis**
You have been provided with a video file at `/app/architecture.mp4`. This video contains a hidden subtitle track (stream 0:s:0) that encodes a dependency graph. 
Extract the text from this subtitle track. The text contains a list of dependencies, one per line, in the format `SourceNode:TargetNode` (meaning `TargetNode` depends on `SourceNode`, so `SourceNode` must be executed first). 

**Part 2: The C Dependency Resolver**
You must write a C program that reads a list of dependencies from `standard input` (one per line, in the `SourceNode:TargetNode` format, until EOF). Node names are alphanumeric strings up to 15 characters long.
The program must perform a topological sort of the graph.
* If multiple nodes have no incoming edges, resolve ties by choosing the node that comes first alphabetically.
* The program must output a valid JSON array of the nodes in their sorted execution order to `standard output`. For example: `["NodeA", "NodeB", "NodeC"]`.
* If the graph contains a cycle (meaning topological sort is impossible), the program must output exactly `{"error": "cycle_detected"}`.

You must provide a `Makefile` in `/home/user/` that compiles your code (e.g., `resolver.c`) into an executable named `/home/user/resolver`. You may use standard C library functions. 

**Part 3: Integration**
Run the dependencies you extracted from `/app/architecture.mp4` through your compiled `/home/user/resolver` binary.
Save the resulting JSON output to exactly `/home/user/video_graph_result.json`.

**Testing and Constraints:**
Your binary will be tested aggressively against a reference implementation using property-based fuzzing. It must exactly match the JSON output of the oracle for thousands of random graphs (both Directed Acyclic Graphs and graphs with cycles). Ensure your JSON formatting (spacing, quotes, newlines) is standard and clean. Do not output anything to `stdout` other than the final JSON payload.