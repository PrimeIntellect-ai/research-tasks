I need help debugging a multi-service integration test build that is currently failing due to severe performance degradation and occasional deadlocks under high contention. 

We have a data pipeline deployed under `/app/` with three components:
1. A Redis instance acting as a message broker.
2. A FastAPI web service (`/app/api.py`) running on port 8000 that receives payloads and pushes them to Redis.
3. A multi-threaded Python worker (`/app/worker.py`) that pops tasks from Redis and processes them concurrently.

Currently, when we hit the API with high concurrency, the worker stalls. I suspect there is a thread contention issue, a deadlock in how the worker manages Redis connections, or a misconfiguration in our environment variables (`/app/.env`).

Your tasks:
1. Diagnose and fix the bottleneck/deadlock in `/app/worker.py`. The worker must safely handle high concurrency without stalling.
2. Fix any environment misconfigurations in `/app/.env` that are contributing to connection starvation.
3. Construct a statistical regression test script at `/app/verify_throughput.py`. This script should:
   - Send 500 requests to `http://127.0.0.1:8000/enqueue` concurrently.
   - Wait for the queue to drain.
   - Calculate the end-to-end throughput.
   - Save the raw throughput float value (tasks per second) to `/home/user/throughput_result.txt`.

The automated verifier will start the services using `/app/start_services.sh`, wait 5 seconds, and then evaluate the system's throughput using a rigorous benchmarking tool. You must ensure the worker processes tasks fast enough to meet our integration pipeline's threshold.