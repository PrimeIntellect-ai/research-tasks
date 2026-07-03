You are a platform engineer responsible for maintaining our custom CI/CD pipeline tools. Our legacy dependency resolution tool was accidentally deleted, and the Python package that wraps it (`/app/dep_resolver`) has a broken build configuration.

We need to reconstruct the core dependency resolution logic, analyze a recovered build artifact, and prepare a robust replacement CLI tool.

**Step 1: Extract Graph from Video Artifact**
We recovered a video artifact of the last successful build state at `/app/pipeline_state.mp4`. The video is exactly 100 frames long. It encodes a 10x10 adjacency matrix of our core build targets:
- Each frame corresponds to a cell in the 10x10 matrix, in row-major order.
- A predominantly black frame (average pixel brightness < 128) represents a `0` (no dependency).
- A predominantly white frame (average pixel brightness >= 128) represents a `1` (a directed edge from target `row` to target `column`).
Using `ffmpeg` or any suitable tool, extract this 10x10 adjacency matrix. 

**Step 2: Implement Dependency Resolver Tool**
You must write a command-line tool located at `/home/user/resolver_cli`. This tool can be written in any language of your choice, but it must be an executable binary or an executable script with a proper shebang.
- **Input:** A single command-line argument consisting of a binary string (e.g., `010010111...`) representing an $N \times N$ adjacency matrix (where $N^2$ is the length of the string, $N \le 50$).
- **Output:** The tool must compute the **lexicographically first topological sort** of the Directed Acyclic Graph. The nodes are 0-indexed (0 to N-1). 
- Print the sorted node indices as a space-separated list to standard output.
- If the graph contains a cycle (meaning dependencies cannot be resolved), print exactly: `CYCLE DETECTED` to standard output.

**Step 3: Analyze the Recovered Graph**
Run your `/home/user/resolver_cli` on the 100-bit string extracted from `/app/pipeline_state.mp4`.
Save the exact standard output to `/home/user/video_result.txt`.

Ensure your executable at `/home/user/resolver_cli` is fast and perfectly matches standard topological sort constraints, as it will be rigorously tested against thousands of randomly generated dependency graphs in our automated QA pipeline.