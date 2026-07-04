You are an infrastructure engineer automating the provisioning of a high-throughput background job processing system on a single node. 

We are using `huey`, a Python task queue. A specific version of the source code for this package is pre-vendored at `/app/huey-src/`. 

Your objectives are:

1. **Fix the Package Performance Bug:**
   The vendored `huey` package contains a deliberate performance perturbation introduced by a previous developer for "debugging". This perturbation drastically slows down the consumer loop. You must locate this bottleneck in the source code under `/app/huey-src/`, remove it, and install the fixed package into your local Python environment.

2. **Implement the Application:**
   Create a Python file at `/home/user/app.py` that configures a `SqliteHuey` instance.
   - The Huey instance must be named `huey` and use a SQLite database located at `/home/user/huey.db`.
   - Define a Huey task (using the `@huey.task()` decorator) named `process_data` that takes an integer `n`, computes the SHA256 hash of the string representation of `n` exactly 100 times, and returns the final hash.

3. **Configure Process Supervision:**
   Create a user-level systemd service to manage the Huey consumer.
   - Create the service file at `/home/user/.config/systemd/user/huey-worker.service`.
   - The service should execute the `huey_consumer.py` script targeting `app.huey`.
   - Configure the consumer to run with 4 worker threads/processes.
   - Set a restart policy so the service always restarts on failure, with a 3-second delay.
   - Start and enable the service using `systemctl --user`.

4. **Run the Benchmark:**
   We have provided a benchmark script at `/app/benchmark.py`. This script queues 5000 `process_data` tasks and measures how long your supervised consumer takes to process all of them.
   - Run `/app/benchmark.py`.
   - Redirect the standard output of this benchmark script to `/home/user/benchmark_result.txt`.
   
The automated test will evaluate your setup based on the time recorded in `/home/user/benchmark_result.txt`. You must achieve a total processing time of less than 4.0 seconds. Ensure your systemd service is active, the bug is fixed, and the workers are efficiently processing the tasks.