I am a researcher running a distributed Monte Carlo simulation pipeline for a 1D random walk with absorbing boundaries. I have a broken setup and need you to implement the core simulation engine and connect it to my service architecture.

First, you need to write the core simulation engine in Python: `/home/user/sim_core.py`.
The engine must simulate a particle starting at position 0.
It will take 4 command-line arguments in this exact order: `N_steps` (integer), `seed` (integer), `p_right` (float), and `L` (integer).
- `N_steps`: maximum number of steps to simulate.
- `seed`: the random seed. You MUST initialize the random state exactly once at the start of the script using `import random; random.seed(seed)`.
- `p_right`: the probability of moving right (+1) in a given step. The probability of moving left (-1) is `1 - p_right`.
- `L`: the absorbing boundary limit. If the particle's absolute position reaches `L` (i.e., `pos == L` or `pos == -L`), the simulation stops immediately.

For each step (from 1 up to `N_steps`):
- Generate a random float `r = random.random()`.
- If `r < p_right`, `pos += 1`. Else, `pos -= 1`.
- If `abs(pos) == L`, break.

The script must print exactly one line to standard output when finished:
`RESULT: <steps_taken>, <final_position>`
(where `<steps_taken>` is the actual number of steps simulated before absorption or reaching `N_steps`).

Second, I have a multi-service architecture located in `/app/`.
- A Redis instance runs on `localhost:6379`.
- A Flask API runs on `localhost:5000`.
You need to write a shell script `/home/user/worker.sh` that acts as the pipeline glue. It should:
1. Block and pop a job from the Redis list `job_queue` (format: `job_id|N_steps|seed|p_right|L`). You can use `redis-cli blpop job_queue 0`.
2. Parse the job parameters.
3. Run `python3 /home/user/sim_core.py` with those parameters.
4. Take the output string, construct a JSON payload `{"job_id": "<job_id>", "output": "<the_stdout_from_sim>"}`.
5. POST this JSON to `http://localhost:5000/submit` with `Content-Type: application/json`.
6. Loop forever.

Please create both `/home/user/sim_core.py` and `/home/user/worker.sh` and make them executable. Our automated validation pipeline will first fuzz-test your `sim_core.py` against our compiled C++ oracle for bit-exact behavioral equivalence over thousands of seeds. Then, it will spin up the Redis and Flask services and push real workloads to verify your `worker.sh` integration end-to-end.