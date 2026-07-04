You are acting as an AI assistant to a compliance officer. We are currently auditing our physical access control systems. Our old SQL-based system for tracing employee movement generated massive false positives due to an implicit cross join in the event logs, making it look like every employee accessed every restricted zone.

To fix this, we are moving to a strict graph-based traversal approach written in C.

**Part 1: Video Log Extraction**
We have a backup of the system's access console recorded as a video at `/app/access_logs.mp4`. 
1. Use `ffmpeg` and OCR tools (like `tesseract`, which is pre-installed) to extract the text from the video. The video shows exactly 1 log entry per second (extract frames at 1 fps).
2. The extracted text will contain access records in the format: `ACCESS: [NODE_U] -> [NODE_V] [WEIGHT]`.
3. Save the successfully parsed edges into a file `/home/user/extracted_edges.txt`.

**Part 2: Compliance Checker C Program**
You must write a C program that acts as our new compliance checker. It needs to read a graph definition and compute the shortest path between nodes to verify if an illicit path exists.
Create your source file at `/home/user/checker.c` and compile it to `/home/user/checker`.

**Input Format (via `stdin`):**
1. Two integers `V` (number of vertices, 1 to 1000) and `E` (number of edges).
2. `E` lines follow, each with three integers `u v w`, representing a directed edge from `u` to `v` with traversal time `w` (vertices are 0-indexed).
3. One integer `Q` (number of queries).
4. `Q` lines follow, each with two integers `start target`.

**Output Format (to `stdout`):**
For each of the `Q` queries, print a single line containing the shortest path distance from `start` to `target`. If `target` is completely unreachable from `start`, output `-1`.

Your compiled binary (`/home/user/checker`) will be tested extensively against an automated fuzzing suite that compares it with our verified, stripped reference binary to ensure BIT-EXACT equivalence. Optimization is critical, as is ensuring you don't leak memory or print extra debugging text during the fuzzing phase.