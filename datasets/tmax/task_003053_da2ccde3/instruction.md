You are a performance engineer tasked with profiling and debugging a multi-service backend application. The system processes streaming statistical data and consists of three components running locally:

1. A Redis instance (message broker).
2. A Data Ingestion API (`/home/user/app/api.py`) running on FastAPI, which generates batches of synthetic float arrays and queues them.
3. An Optimization Worker (`/home/user/app/worker.py`) that pulls the arrays from Redis, decodes them, and runs a gradient descent algorithm to compute a geometric median.

**The Problem:**
The worker is currently experiencing a severe performance bottleneck. Processing a standard batch of 100 tasks takes over 40 seconds. By investigating, you will find that the gradient descent algorithm is failing to converge and is hitting its maximum iteration limit (`max_iter=5000`) on every single task. 

Initial statistical anomaly investigation suggests the data arriving at the optimization step is corrupted (containing massive, unrealistic outliers). You suspect an encoding and serialization mismatch between how the API packs the data and how the worker unpacks it from the Redis queue.

**Your Tasks:**
1. **Start the environment:** You can start the mock environment using the provided `/home/user/app/start_services.sh` script, which launches Redis, the API, and the worker. (You will need to install any missing dependencies like `fastapi`, `uvicorn`, `redis`, and `numpy`).
2. **Debug and Fix:** Identify the root cause of the convergence failure. Fix the serialization/decoding bug in either `/home/user/app/api.py` or `/home/user/app/worker.py`.
3. **Regression Test:** Create a regression test file at `/home/user/app/test_serialization.py` that contains a function `test_roundtrip()`. This test should simulate the exact encoding step used in `api.py` and the decoding step used in `worker.py`, asserting that the input NumPy array `[1.5, -2.3, 3.14]` perfectly matches the decoded array.
4. **Performance verification:** Once fixed, the worker should be able to process 100 tasks in less than 3 seconds, because the gradient descent will converge in just a few iterations on healthy data.

You can modify the source code of the API and worker as needed.