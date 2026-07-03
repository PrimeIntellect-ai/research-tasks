You are a mobile build engineer maintaining the CI/CD pipeline for a video processing application. Our current webhook router that triggers build jobs is a legacy C binary (`/app/oracle_router`) that suffers from memory corruption when parsing malformed URLs, and it lacks proper path-traversal protections. 

Your task is to safely translate this legacy component into a Python script located at `/home/user/safe_router.py`.

The script must accept exactly one command-line argument: a webhook URL.

**URL Routing & Parameter Parsing:**
The URL will look like this:
`https://ci.local/build/trigger?video=/app/pipeline_test.mp4&nodes=A:1.0,B:2.5,C:1.5&edges=A->B,C->B`

1. **Validation**: The URL schema must be `https`, the domain must be `ci.local`, and the path must be `/build/trigger`. The `video` parameter must strictly resolve to a file inside the `/app/` directory (reject any path traversal attempts like `../` or symlink escapes).
2. **Nodes**: A comma-separated list of nodes. Each node format is `NodeName:Timestamp` (e.g., `A:1.0`). `Timestamp` is a float representing seconds. Node names are alphanumeric.
3. **Edges**: A comma-separated list of dependencies `Src->Dst`. This means `Src` must run *before* `Dst`.

**Graph Traversal & Dependency Resolution:**
You must parse the `nodes` and `edges` to construct a Directed Acyclic Graph (DAG). 
Compute a topological sort of the nodes to determine the execution order. If multiple nodes have no dependencies at any step, break ties by sorting them alphabetically by node name.
If a cycle is detected, or if the URL is invalid based on the validation rules, or if an edge references a non-existent node, the process must abort.

**Video Processing Integration:**
For each node in the resolved execution order, you must analyze a frame from the specified `video` file.
1. Extract the exact frame at the specified `Timestamp` using `ffmpeg`. 
2. Convert the frame to grayscale and calculate the arithmetic mean of all pixel intensities (from 0 to 255).
3. Truncate the mean to an integer.

**Output Format:**
Your script must print a single JSON line to standard output.
If successful:
`{"status": "success", "order": ["A", "C", "B"], "results": {"A": 125, "C": 45, "B": 210}}`
If any validation fails, a cycle is detected, or the video file cannot be read safely:
`{"status": "error"}`

Your implementation will be exhaustively fuzzed against the reference oracle with hundreds of randomly generated URLs to ensure it is bit-for-bit identical in behavior, error handling, and output.