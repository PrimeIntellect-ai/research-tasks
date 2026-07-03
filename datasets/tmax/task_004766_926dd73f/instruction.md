We have a long-running event ingestion pipeline deployed in `/home/user/pipeline`. The system consists of three services:
1. An Nginx reverse proxy
2. A Python Flask application
3. A Redis cache

Currently, the system is failing. The Nginx reverse proxy is returning 502 Bad Gateway or 404s, the Flask app cannot connect to Redis, and even when bypassed, the Flask app exhibits a memory leak and intermittent crashes due to a timezone parsing bug.

Your tasks are:
1. **Fix the Integration**: 
   - Modify the Nginx configuration (`/home/user/pipeline/nginx/nginx.conf`) so that requests to `http://localhost:8080/api/ingest` correctly route to the Flask app on port 5000 (the Flask app expects the path `/ingest`).
   - Fix the Flask app's configuration in `/home/user/pipeline/flask/app.py` so it connects to the Redis instance correctly (Redis is running on localhost:6379).
   
2. **Fix the Parsing Bug & Memory Leak**:
   - The Flask app uses a module located at `/home/user/pipeline/flask/time_parser.py` to parse incoming timestamp strings.
   - The current implementation of `time_parser.py` has a naive caching mechanism that causes a memory leak and fails on certain edge-case timezone formats (e.g., un-normalized timezone strings).
   - We have provided a perfectly working, memory-safe reference implementation compiled as a Python bytecode file at `/app/oracle_time_parser.pyc`. 
   - You must debug and rewrite the `parse_and_normalize(time_str)` function in `/home/user/pipeline/flask/time_parser.py` so that its input/output behavior and error handling are **bit-exact equivalent** to the `parse_and_normalize` function in `/app/oracle_time_parser.pyc`.

Ensure that you start the services using `/home/user/pipeline/start.sh` and verify the end-to-end flow. You can test the endpoint by sending a POST request with JSON `{"time": "2023-10-12T15:30:00Z"}` to `http://localhost:8080/api/ingest`.

Leave the finalized `time_parser.py` in `/home/user/pipeline/flask/time_parser.py`.