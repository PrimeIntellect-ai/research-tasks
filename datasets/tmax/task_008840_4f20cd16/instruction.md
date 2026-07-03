You are helping a computational researcher fix a flaky network optimization simulation. The script evaluates the cost of a network design and optimizes the node capacities using gradient descent.

However, the researcher is running into two issues:
1. **Flaky Regression Tests:** The total loss calculation is non-deterministic across different runs. This happens because the script iterates over an unordered `set` of network edges, causing floating-point accumulation differences due to reduction order. 
2. **Incomplete Optimization:** The gradient descent update step for node capacities is missing.

Your tasks:
1. Inspect the script `/home/user/network_sim.py`.
2. Fix the `compute_total_loss` method. Make it completely deterministic by sorting the edges by their `source` node ID, then by their `target` node ID, before summing their weights. (Do not change the edges set to a list permanently, just sort it during the calculation).
3. Complete the `optimize_node_capacities` method. Implement standard gradient descent. For each node `i`, the local loss is `(capacity[i] - target_capacity[i])**2`. The gradient with respect to `capacity[i]` is `2 * (capacity[i] - target_capacity[i])`. Update the capacities using the provided `learning_rate`.
4. Run the regression test script provided at `/home/user/test_sim.py` to ensure your fixes work and the output is deterministic.
5. Execute the main block of `/home/user/network_sim.py` and save the final total loss (after optimization) to `/home/user/final_loss.txt`. The value should be formatted to exactly 6 decimal places (e.g., `12.345678`).

Ensure you have written the exact output to the text file. You can install any standard testing libraries like `pytest` if you wish to run the tests that way, or just run the test script directly with Python.