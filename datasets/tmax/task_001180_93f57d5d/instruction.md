You are acting as a performance engineer troubleshooting a distributed scientific computing system. The system runs numerical simulations of DNA sequence evolution models. Recently, some simulation jobs have been diverging due to incorrect step-size adaptation in the numerical integrator, causing the workers to stall.

Your objective has two parts:

Part 1: Service Composition
The system consists of three services located in `/home/user/simulation_app/`:
1. A Redis message queue.
2. A Flask API (`api.py`) that accepts simulation jobs.
3. An MPI-based worker daemon (`worker.py`) that executes the jobs.

Currently, the startup script `/home/user/simulation_app/start_services.sh` is broken. The services cannot communicate. 
- You must fix the configuration (environment variables and connection strings in `start_services.sh` and the python scripts) so that the Flask API correctly listens on port `5050`, the Redis server runs on port `6379`, and the `worker.py` connects to Redis at `localhost:6379`.
- When correctly configured, running `curl -X POST http://localhost:5050/submit -d '{"job": "test"}'` should result in the MPI worker logging a successful job execution to `/home/user/simulation_app/worker.log`.

Part 2: Adversarial Trace Classifier
We need a tool to automatically identify diverging simulations based on their execution traces. 
In `/home/user/corpus/`, you will find two directories:
- `/home/user/corpus/clean/`: Contains CSV trace files of simulations that converged successfully.
- `/home/user/corpus/evil/`: Contains CSV trace files of simulations that diverged due to step-size collapse.

The CSV files have columns: `step, time, dt, error`. In diverging traces, the step size `dt` repeatedly drops to extremely small values (e.g., $< 10^{-6}$), altering the overall density distribution of `dt`.

Write a Python script at `/home/user/trace_classifier.py` that takes a single file path as an argument:
`python /home/user/trace_classifier.py <path_to_csv>`

Your script must:
1. Load the CSV data and perform density estimation (e.g., KDE or histogram analysis) on the `dt` column.
2. Output EXACTLY the string `CLEAN` to standard output if the trace is well-behaved.
3. Output EXACTLY the string `EVIL` to standard output if the trace exhibits step-size divergence.
4. Save a KDE plot of the `dt` distribution as `/home/user/latest_plot.png` (overwrite if exists) for visual inspection.

Constraints:
- You must achieve 100% accuracy on both the clean and evil corpora.
- Use Python as the primary language.