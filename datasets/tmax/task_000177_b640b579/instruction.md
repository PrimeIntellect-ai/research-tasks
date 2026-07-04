You are a support engineer tasked with diagnosing and fixing a physics simulation that is crashing in production.

A customer reported that their containerized simulation job is failing. They have provided you with the simulation script, their input data, and the container logs from the failed run.

You will find the following files in `/home/user/sim_env`:
- `sim.py`: The Python simulation script.
- `inputs.csv`: The dataset containing initial particle positions.
- `container_crash.log`: The log output from the failed production container.

Your objectives:
1. **Fix the Infinite Recursion:** Analyze `container_crash.log` and `sim.py`. The simulation uses a recursive time-stepping function that has a boundary condition bug (off-by-one/floating-point issue), causing it to hit the recursion limit. Fix this in `sim.py` so it strictly terminates when the simulation time `t` reaches or exceeds `max_t`.

2. **Minimize the Test Case:** Once the recursion bug is fixed, running `python sim.py inputs.csv` will reveal a *new* crash—a numerical instability (`ValueError`) caused by catastrophic cancellation in the variance calculation. Before fixing it, you must isolate the problem. Write a delta-debugging script to find the *minimal contiguous subset of lines* (minimum 2 lines required to compute variance) from `inputs.csv` that still triggers this exact `ValueError`. Save these minimal crashing lines exactly as they appear to `/home/user/sim_env/minimal_crash.csv`.

3. **Fix the Numerical Instability:** Update the variance calculation in `sim.py` to be numerically stable (e.g., use Welford's method, or a stable library function like `statistics.variance`) so it doesn't fail on data with large means and small variances.

4. **Generate Final Output:** Run your fully fixed `sim.py` on the complete `inputs.csv`. Save the standard output (which should just be the final calculated standard deviation) to `/home/user/sim_env/success.txt`.

Ensure your fixes in `sim.py` don't change the intended physics calculations (each position should still step by `1.5 * dt` per step).