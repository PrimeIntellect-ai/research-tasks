I need you to complete a complex data processing and migration task for our legacy Python 2 dependency resolver. We are migrating to Python 3, but the codebase currently has a circular import preventing it from running, and we lost the most recent patch file. Fortunately, a video of the terminal output containing the QR-encoded patches was recovered.

Your objectives:

1. **Extract and Reconstruct the Patch (Diff/Patch Processing)**
   - A video file is located at `/app/dependency_patches.mp4`.
   - The video runs at 1 FPS. Extract the frames and read the QR codes from them (using `zbarimg` and `ffmpeg` or similar tools).
   - The decoded text from the QR codes contains chunks of a base64-encoded unified diff. Concatenate the decoded base64 strings in chronological order (frame 1, frame 2, etc.) and decode them to retrieve the patch file.
   - Apply this patch to the Python 2 codebase located in `/home/user/legacy_resolver/`.

2. **Migrate to Python 3 and Fix the Architecture**
   - The `/home/user/legacy_resolver/` codebase uses Python 2 constructs (e.g., `print` statements, `xrange`, `iteritems`). Migrate the codebase to run under Python 3.
   - The patch you applied attempts to fix a circular import between `graph.py` and `nodes.py`, but it leaves behind a logical circular dependency in the graph resolution logic. 
   - Analyze the graph traversal algorithm in `resolver.py`. You must fix the algorithm so it correctly breaks circular dependency ties by prioritizing nodes with alphabetically earlier names (Constraint Satisfaction & Graph Traversal).

3. **Expose as a CLI for Fuzz Testing**
   - We need to verify your fixed resolver against our compiled oracle.
   - Create a final Python 3 executable script at `/home/user/run_resolver_v3.py`.
   - This script must read a JSON payload from `stdin`. The payload will be a dictionary representing a directed graph (e.g., `{"A": ["B", "C"], "B": ["C", "A"], "C": []}`).
   - The script must traverse the graph starting from the alphabetically first node, resolving the nodes in topological order. Because the graph may contain cycles, it must use the updated logic to break cycles (drop the edge that causes the back-edge, prioritizing alphabetical traversal).
   - The script must print a single valid JSON list of the resolved nodes to `stdout` (e.g., `["A", "B", "C"]`) and exit with code 0.
   - Ensure the script runs quickly and efficiently, as it will be heavily tested against large graphs. Ensure no debug output is printed to `stdout` during the final run.

Make sure the final executable is exactly at `/home/user/run_resolver_v3.py` and has executable permissions (`chmod +x`). Do not include any hardcoded data; the script must dynamically process the `stdin` input.