You are a script developer on a web security team. We are migrating our legacy Access Control system into a microservices architecture. Our core security transition logic is currently locked inside an old, stripped, undocumented compiled shared object, which evaluates whether a user's authorization token allows them to transition between different types of web resources.

Your task is to build a modern Python HTTP service that wraps this legacy engine and uses it to perform full attack-path analysis (graph traversal) over a web application's asset dependency graph.

**Components & Requirements:**

1. **The Legacy Binary:** 
   You have been provided a stripped shared library at `/app/libsec_eval.so`. 
   - Analyze this binary to find its exported validation function. The function takes three C-strings as arguments: the "from" resource type, the "to" resource type, and an "auth_token". It returns a standard C integer (`1` if the transition is allowed by the token, `0` if denied).
   - You must use Python's FFI capabilities (`ctypes`) to load this library and call the function.

2. **The Python HTTP Service:**
   - Create a Python web service (using `http.server`, `Flask`, or `FastAPI` - whatever you prefer, provided it runs on standard library or you install dependencies locally in a virtual environment if needed).
   - The service must listen on exactly `127.0.0.1:8000`.
   - Expose a single endpoint: `POST /api/v1/analyze_path`.
   - The endpoint will receive a JSON payload detailing a web asset graph, a start node, an end node, and a token:
     ```json
     {
       "nodes": {
         "n1": "PublicPage",
         "n2": "UserDashboard",
         "n3": "AdminPanel"
       },
       "edges": [
         ["n1", "n2"],
         ["n2", "n3"]
       ],
       "source": "n1",
       "target": "n3",
       "token": "USER_TOKEN"
     }
     ```
     *(Note: `nodes` maps a node ID to its resource type. `edges` is a list of directed edges [from_id, to_id]).*

3. **Graph Traversal & Integration:**
   - When the endpoint receives a request, your Python code must traverse the provided graph to determine if a valid path exists from the `source` node to the `target` node.
   - **Crucial Rule:** An edge is only traversable if the legacy C function returns `1` when evaluated with the resource *types* of the corresponding nodes and the provided `token`.
   - The endpoint must return a JSON response: `{"path_exists": true}` if a traversable path exists, and `{"path_exists": false}` otherwise.

4. **Test Fixture Setup:**
   - Write a standalone test script at `/home/user/test_fixture.py` that sends a mock request (representing an attacker trying to pivot from a "Public" node to an "Admin" node) to your running API on port 8000. It should assert the response and print "TEST_PASSED" to standard output if successful.

Ensure your Python service is running in the background so it can be automatically verified once you are done.