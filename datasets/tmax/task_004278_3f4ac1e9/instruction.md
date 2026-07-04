You are an engineer tasked with fixing a broken deployment process and optimizing its service scheduler. 

A custom Python-based service supervisor previously ran a set of 5 background tasks (Task A, B, C, D, and E). Currently, it attempts to run them all sequentially or in the wrong order, causing missing dependency errors and taking over 15 seconds to complete. 

You have been given a diagram of the correct service architecture in `/app/architecture.png`.

Your objectives:
1. **Analyze Dependencies:** Read the architecture diagram in `/app/architecture.png` to understand the required execution order (DAG) of the tasks.
2. **Implement an Asynchronous Scheduler:** Write a Python script at `/home/user/scheduler.py` that executes the tasks (`/home/user/tasks/task_{A,B,C,D,E}.py`) in the correct topological order. Independent tasks MUST be run in parallel to minimize overall startup time.
3. **Log Configuration & Rotation:** The tasks generate substantial log output. Your `scheduler.py` must capture the standard output of each task and write it to `/home/user/logs/<task_name>.log`. Implement a log rotation mechanism in your scheduler that rotates files when they exceed 1MB, keeping a maximum of 3 compressed (`.gz`) backups per task.
4. **Error Handling:** If any task exits with a non-zero status, the scheduler should immediately terminate dependent tasks but allow independent parallel tasks to finish.

The system will verify your solution by measuring the total execution time of `python3 /home/user/scheduler.py`. To pass, your implementation must complete the workload optimally, achieving a total runtime threshold.

*Constraints:*
- Do not modify the existing task scripts in `/home/user/tasks/`.
- Use Python's built-in libraries (e.g., `asyncio`, `subprocess`, `logging`, `gzip`).
- Ensure the final script is executable and fully self-contained.