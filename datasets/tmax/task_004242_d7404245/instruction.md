I am migrating a legacy Python 2 background service to Python 3, but I'm hitting a wall with an old C-extension and needing to modernize the API. 

The project is located at `/home/user/scheduler_service/`. I have created a skeleton project with the legacy C-extension. 

Here is what you need to do:

1. **Fix the C-extension for Python 3:**
   The C-extension is located at `/home/user/scheduler_service/job_hasher.c`. It takes a list of strings (job IDs) and computes a simple hash. During the Python 3 migration, someone blindly changed `PyString_AsString` to `PyBytes_AsString`, but in Python 3, string objects are Unicode. Calling `PyBytes_AsString` on a Unicode object causes undefined behavior and segfaults. 
   - Modify `job_hasher.c` to safely extract the C string from Python 3 Unicode objects.
   - Build and install the extension in the environment (a `setup.py` is provided).

2. **Implement the API Server:**
   Write a Python 3 REST API using Flask or FastAPI in `/home/user/scheduler_service/server.py`.
   The server should run on `127.0.0.1:8080` and expose a single endpoint: `POST /allocate`.

3. **Implement Constraint Satisfaction (Interval Scheduling):**
   The `POST /allocate` endpoint will receive a JSON payload containing a list of jobs with start and end times.
   Example input:
   ```json
   {
     "jobs": [
       {"id": "A", "start": 1, "end": 4},
       {"id": "B", "start": 3, "end": 5},
       {"id": "C", "start": 4, "end": 7}
     ]
   }
   ```
   - Your code must find the maximum number of mutually compatible (non-overlapping) jobs. A job starts at `start` and ends at `end`. Two jobs do not overlap if one ends before or at the exact time the other starts (e.g., end 4 and start 4 do not overlap).
   - Use the standard greedy approach: always pick the compatible job that ends earliest.
   - Extract the list of `id`s of the scheduled jobs.
   - Call the fixed `job_hasher` C-extension with this list of IDs to get the integer hash.

4. **API Response:**
   Return a JSON response with the following format:
   ```json
   {
     "scheduled_jobs": ["A", "C"],
     "hash": 134
   }
   ```

5. **Verification:**
   Once your server is running, use `curl` to send a POST request to `http://127.0.0.1:8080/allocate` with this exact payload:
   `{"jobs": [{"id": "J1", "start": 0, "end": 6}, {"id": "J2", "start": 1, "end": 4}, {"id": "J3", "start": 5, "end": 7}, {"id": "J4", "start": 4, "end": 8}, {"id": "J5", "start": 8, "end": 10}]}`
   
   Save the exact raw JSON output from `curl` to `/home/user/scheduler_service/result.json`.

Please run the server in the background so you can execute the curl command and save the result. Let me know when `/home/user/scheduler_service/result.json` is ready.