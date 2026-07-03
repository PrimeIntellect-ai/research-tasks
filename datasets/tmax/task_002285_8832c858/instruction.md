You are a DevOps engineer investigating a critical data corruption issue in our newly deployed log processing pipeline. 

Recently, we upgraded our logging system to record timestamps in millisecond precision (previously they were in seconds). Since this change, our analytics dashboard is showing bizarre, often negative latency values, and dropping thousands of log entries. The original author claimed the pipeline "worked fine on their machine" but it's failing in our production environment.

The system consists of multiple microservices located in `/home/user/log_pipeline`:
1. **Redis**: Used as a message broker for incoming log events.
2. **API (Flask)**: Receives log payloads via HTTP and pushes them to Redis. Runs on port 5000.
3. **Worker**: A Python daemon that pulls events from Redis in batches, calculates request latencies and aggregates them using NumPy, and writes the output to `/home/user/log_pipeline/output/metrics.json`.

Your tasks:
1. Start the system by running `/home/user/log_pipeline/start_services.sh`. You can verify the API is up by checking `http://127.0.0.1:5000/health`.
2. Inspect `worker.py` and figure out why latencies are being computed as negative numbers or dropping entirely. Fix the bug in `worker.py`.
3. The system needs to be highly reliable. Write a regression test script at `/home/user/log_pipeline/regression_test.py` that pushes a batch of mock log entries (with millisecond timestamps) to the Flask API, waits 2 seconds, and asserts that the resulting latencies in `metrics.json` are positive and correct.
4. Ensure the system works end-to-end. 

For verification, our automated testing suite will run a grader script that pushes 10,000 log events with millisecond timestamps to your fixed pipeline and calculates an accuracy metric. The metric is defined as the ratio of correctly calculated latencies to the total number of events. You must achieve an accuracy of 1.0 (100%).

Note: You do not have root access, but all necessary tools (python3, pip, redis-server) are available or can be installed in your local user environment.