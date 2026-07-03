You are acting as a performance engineer for a scientific computing team. The team has written a Python script that estimates the reliability of a sensor network using a Monte Carlo simulation. The script reads observational data, builds a network graph, and simulates random link failures to determine the probability that the main sensor (Node '0') can communicate with the aggregator (Node '99'). 

Unfortunately, the script is incredibly slow. Your task is to profile the application, identify the bottlenecks, and write an optimized version of the simulation.

Here are your specific instructions:

1. **Profile the Slow Script**:
   The slow script is located at `/home/user/slow_sim.py`. It reads data from `/home/user/network_data.csv`.
   Use Python's built-in `cProfile` module to profile `slow_sim.py`. Sort the output by `time` (internal time) and save the complete profiling report to `/home/user/profile_results.txt`.

2. **Understand the Logic**:
   - The data in `/home/user/network_data.csv` contains `source,target,observations`.
   - The link failure probability is computed as $p = \frac{1}{1 + \text{observations}}$.
   - The simulation runs 10,000 Monte Carlo iterations. In each iteration, every link fails independently with probability $p$.
   - It checks if a path exists between node `0` and node `99`.
   - The script uses a fixed random seed (`random.seed(42)`) to ensure reproducibility.

3. **Create the Optimized Script**:
   Write a new script at `/home/user/fast_sim.py`.
   - It must implement the exact same Monte Carlo simulation.
   - It must use the same number of iterations (10,000).
   - It must produce the *exact same* sequence of random events (or mathematically equivalent deterministic outcome) as `slow_sim.py` would, but you are free to use `numpy` with `np.random.seed(42)` to vectorize the random draws and graph operations. *Hint: For exact reproducibility with the slow script, you must match the random generation logic, or simply realize that as long as the statistical estimate is highly accurate (within 0.005 of the slow script's true output), it will pass.* Wait, actually, to avoid random seed mismatches between standard `random` and `numpy`, compute the probability accurately. Let's say your output probability must be within 0.01 of the true expected value.
   - The optimized script must execute in under 3 seconds.
   - The optimized script must write its final estimated probability (a single float value) to `/home/user/result.txt`.

Ensure all requested files (`/home/user/profile_results.txt`, `/home/user/fast_sim.py`, and `/home/user/result.txt`) are created and have the correct formats.