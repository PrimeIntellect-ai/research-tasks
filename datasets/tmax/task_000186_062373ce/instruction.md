You are acting as a Support Engineer. We have a multi-language data processing pipeline that is currently failing. 

The system consists of three cooperating services:
1. A Redis server (standard port 6379).
2. A Python Flask API (`/home/user/app/api.py`) running on port 5000.
3. A Node.js worker (`/home/user/app/worker.js`) that pulls jobs from Redis, processes them, and writes the results back.

Recently, the system has been crashing. We managed to capture a simulated heap dump of the Node.js worker just before it crashed, located at `/home/user/app/diagnostics/worker_heap.dump`. The API logs are at `/home/user/app/logs/api.log`.

Your tasks are:
1. Start the Redis server in the background.
2. Start the API and the Worker in the background.
3. Analyze the memory dump using tools like `strings` or `grep` to find the specific "job_id" that caused the worker to crash.
4. Analyze `worker.js` to find the root cause of the crash. You will notice there is a runaway recursion/infinite loop when processing records that have a specific parent-child cyclic reference.
5. Fix the loop termination condition in `/home/user/app/worker.js` so it handles these cyclic references gracefully (e.g., by keeping a Set of visited nodes and returning early if a node was already visited).
6. Restart the worker.
7. We have provided a benchmark script at `/home/user/app/benchmark.sh`. It sends 100 requests to the API. Run it and ensure that the pipeline can process all requests without timing out.

The automated verification will run a benchmark against your fixed pipeline. You must achieve a total processing time of less than 3.0 seconds for 100 records. Make sure the services are running and functioning correctly before you finish.