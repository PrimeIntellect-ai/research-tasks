You are a performance engineer tasked with optimizing a slow statistical profiling workload. 

Currently, our system relies on a Monte Carlo sampling approach to find the optimal configuration parameters $(X, Y)$ that minimize a specific cost function. 

You are provided with a heavy simulation script at `/home/user/simulate.sh` that takes two arguments `X` and `Y` and outputs the computed cost. Because this simulation mimics a complex workload, it has an artificial delay (`sleep`).

You are also provided with a Monte Carlo sample set of 1000 randomly generated configurations in `/home/user/samples.txt` (each line contains an `X` and `Y` value separated by a space).

Running this sequentially for all 1000 samples takes far too long. Your task is to write a highly optimized Bash script that parallelizes this parameter sweep and finds the best configurations.

**Task Requirements:**
1. Write a Bash script at `/home/user/fast_sweep.sh`.
2. The script must read the configuration points from `/home/user/samples.txt`.
3. It must execute `/home/user/simulate.sh X Y` for each point. You **must** parallelize these executions using `xargs` or GNU `parallel` to ensure the entire sweep completes in under 10 seconds.
4. Collect the output of all simulations.
5. Sort the results based on the `cost` (which is the third column returned by the simulation, after X and Y) in ascending order.
6. Extract the top 3 best configurations (the ones with the lowest cost).
7. Save these top 3 configurations to `/home/user/best_results.txt` in the exact format: `X,Y,cost` (comma-separated, no spaces).

**Constraints & Details:**
- `simulate.sh` outputs lines in the format: `X Y cost`
- Your final output file `/home/user/best_results.txt` must contain exactly 3 lines.
- You must ensure the script handles the parallel output correctly without interleaving text.