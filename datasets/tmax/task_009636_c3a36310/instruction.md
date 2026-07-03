You are an AI assistant helping a data scientist debug a Monte Carlo simulation used for fitting molecular network models. 

The scientist has written a C program that performs random walks on a network graph to compute a "Model Fit Score". They use a fixed random seed, so the simulation should be perfectly reproducible. However, they are seeing slight variations in the floating-point output across multiple runs, which is ruining their observational data reshaping pipeline. They suspect the issue is related to floating-point reduction order caused by multi-threading.

You have access to the following files in `/home/user/sim/`:
- `network_mc.c`: The C source code of the Monte Carlo network simulation.
- `graph.txt`: The input observational data (an edge list of the molecular network).

Your task is to write two Bash scripts to test, measure, and fix this issue using standard Linux CLI tools (bash, awk, sort, etc.).

**Step 1: Quantify the Non-Determinism**
Write a Bash script at `/home/user/test_sim.sh` that does the following:
1. Compiles `/home/user/sim/network_mc.c` into an executable at `/home/user/sim/simulate`. You must link the math library (`-lm`) and enable OpenMP (`-fopenmp`).
2. Runs the executable 100 times.
3. Extracts the floating-point score from the output of each run. The program prints a line like: `Final Score: 12345.678901`
4. Calculates the number of unique scores produced, as well as the minimum and maximum score across the 100 runs.
5. Writes these statistics to `/home/user/sim_stats.txt` in exactly this format:
   `Unique: <N>, Min: <val>, Max: <val>`

**Step 2: Provide a Stable Wrapper**
Write a second Bash script at `/home/user/fix_sim.sh` that:
1. Ensures the simulation runs in a completely reproducible (deterministic) manner without modifying the C source code. (Hint: Look at how OpenMP threading can be controlled via environment variables).
2. Runs the simulation 10 times to verify stability.
3. Extracts the score from the final run and writes it to `/home/user/stable_score.txt` in exactly this format:
   `Stable Score: <val>`

Make sure your scripts have executable permissions. Do not use Python; rely exclusively on Bash and coreutils (awk, grep, sort, wc, etc.).