You are tasked with porting a legacy C-based graph layout tool into a modern, cached REST API using Python. The system needs to be deployed in an environment where fast, repeated access to the same computations is heavily penalized unless properly cached. 

There are multiple services and components involved in `/home/user/app`:

1. **The C Backend Tool (`/home/user/app/backend`)**:
   - Contains a small C project that calculates spring-based graph layouts. 
   - Currently, `make` fails with a linking error. You must fix the `Makefile` so that the tool compiles successfully into an executable named `layout_engine`.
   - Usage: `./layout_engine <input_file>`
   - Input format: Plaintext, where the first line is the number of vertices, followed by lines of `u v` representing edges.
   - Output format: Comma-separated values representing `x,y` coordinates for each vertex.

2. **The Redis Service**:
   - A Redis server is already running on `127.0.0.1:6379`.

3. **The Python REST API (`/home/user/app/api.py`)**:
   - You must write a Python web server (using Flask or FastAPI, both are installed) that listens on `127.0.0.1:8000`.
   - It must expose a single endpoint: `POST /api/layout`
   - **Request format (JSON)**: 
     ```json
     {
       "vertices": 3,
       "edges": [[0, 1], [1, 2], [2, 0]]
     }
     ```
   - **Behavior**: 
     - Serialize the JSON into the format required by `layout_engine`.
     - Execute the compiled `layout_engine` using a subprocess.
     - Parse the CSV output and deserialize it into JSON.
     - **Crucially**, you must implement caching using the local Redis instance. The cache key should be a deterministic string representation of the request payload. If a layout for an identical graph is requested, the API must return the cached JSON result immediately without invoking the C tool.
   - **Response format (JSON)**:
     ```json
     {
       "coordinates": [
         {"x": 1.0, "y": 0.0},
         {"x": -0.5, "y": 0.866},
         {"x": -0.5, "y": -0.866}
       ]
     }
     ```

Your goal is to have the API running continuously in the background on port `8000` (e.g., `python3 /home/user/app/api.py &`) before you finish. The grading system will send an initial request to verify serialization/deserialization correctness, followed by a barrage of 100 identical requests to evaluate your metric score (latency). To pass, the total time for the 100 cached requests must be under 0.5 seconds.