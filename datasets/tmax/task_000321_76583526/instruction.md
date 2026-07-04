You are an assistant helping a computational sociology researcher run network topology simulations. The researcher is using Markov Chain Monte Carlo (MCMC) to sample network graphs with 5 nodes, looking for optimal structural configurations. The energy function of a graph is evaluated by an existing local microservice, but the MCMC sampler and convergence testing must be implemented from scratch in Bash.

Here is what you need to do:

1. **Start the Energy Evaluation Service:**
   There is a Python script located at `/home/user/graph_api.py` that implements a Flask web service. 
   - Install any required dependencies (the script uses `flask`).
   - Run the service in the background so it listens on `http://127.0.0.1:8000`.

2. **Write the MCMC Sampler in Bash:**
   Create a Bash script `/home/user/mcmc_sampler.sh`. The script must take three arguments: a random seed, the number of steps, and the output log file path.
   Usage: `./mcmc_sampler.sh <seed> <steps> <output_file>`
   
   **State Representation:**
   The network has 5 nodes. There are exactly 10 possible undirected edges. 
   Represent the graph state as a 10-character binary string (e.g., `0000000000` is the empty graph, `1111111111` is the complete graph).
   Start the chain at the empty graph `0000000000`.

   **Algorithm for each step:**
   - **Propose** a new state by picking a random index (1 to 10 inclusive) and flipping that bit (0 becomes 1, 1 becomes 0) in the current state string. Use the provided `<seed>` to initialize `awk` or `RANDOM` so the process is deterministic if needed, though pure Bash `$RANDOM` initialized via `RANDOM=$seed` is fine.
   - **Evaluate** the current and proposed state by sending a JSON POST request to the API: 
     `curl -s -X POST -H "Content-Type: application/json" -d '{"graph": "<binary_string>"}' http://127.0.0.1:8000/energy`
     The response will be in the format: `{"energy": 4.25}`. Extract this float value. (Assume the initial state `0000000000` has energy $E_{current}$).
   - **Accept/Reject** using the Metropolis-Hastings criterion:
     - If $E_{proposed} < E_{current}$, accept the proposed state.
     - If $E_{proposed} \ge E_{current}$, accept with probability $P = \exp(E_{current} - E_{proposed})$. Generate a uniform random float between 0 and 1; if it is $< P$, accept. Otherwise, reject (keep the current state).
     *(Hint: You can use `awk` to calculate the math and random floats).*
   - **Log**: Append the energy of the *resulting* state (whether the proposal was accepted or rejected, log the energy of the state you end up with for this step) to `<output_file>`, one float per line.

3. **Perform Convergence Testing:**
   Write a second Bash script `/home/user/run_experiment.sh` that:
   - Runs three independent MCMC chains using your `mcmc_sampler.sh` in the background.
   - Chain 1: seed=101, steps=500, output=`/home/user/chain_1.log`
   - Chain 2: seed=202, steps=500, output=`/home/user/chain_2.log`
   - Chain 3: seed=303, steps=500, output=`/home/user/chain_3.log`
   - Waits for all three chains to finish.
   - Calculates the average energy of the **last 100 steps** across all three chains combined (i.e., a single mean value of those 300 data points).
   - Writes this final floating-point average to `/home/user/convergence_result.txt`.

Ensure your scripts are executable. Run `/home/user/run_experiment.sh` to generate the logs and the final `convergence_result.txt`.