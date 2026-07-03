You are a bioinformatics analyst working on a protein-protein interaction network simulation. 

We have a Python script `/home/user/simulate_diffusion.py` that calculates a stationary probability distribution of a signal diffusing through a network, using a node-level accumulation algorithm. The network is stored in `/home/user/ppi_network.csv`.

**The Problem:**
Due to Python's hash randomization, the iteration order over sets changes across different executions of the script. Because floating-point addition is not strictly associative, this non-deterministic iteration order causes the final probability distribution to vary slightly between runs. We need reproducible computation pipelines for our regulatory submissions.

**Your Tasks:**
1. Execute the *original* `simulate_diffusion.py` twice and capture its JSON output (a dictionary mapping node IDs to probabilities).
2. Calculate the Jensen-Shannon Divergence (JSD) between the probability distributions produced by these two runs. Save this single floating-point value to `/home/user/jsd_original.txt`. You may use `scipy.spatial.distance.jensenshannon` for this.
3. Identify the bug in `/home/user/simulate_diffusion.py` causing the non-deterministic float accumulation and modify the script to fix it. Make sure the logic remains mathematically equivalent, just strictly ordered.
4. Execute your *fixed* script twice.
5. Calculate the JSD between the two fixed runs, and save this single floating-point value to `/home/user/jsd_fixed.txt`.

**Important Constraints:**
* Do not change the random seed environment variables. The script must be intrinsically reproducible regardless of hash seeds.
* Do not alter the fundamental math, just ensure deterministic reduction order.
* The output JSON maps node IDs (strings) to probabilities (floats). When calculating JSD, ensure you align the arrays by node ID keys alphabetically.
* JSD is symmetric; just output the base-e JSD value.

**Final expected state:**
- `/home/user/simulate_diffusion.py` is patched.
- `/home/user/jsd_original.txt` contains a float greater than 0.
- `/home/user/jsd_fixed.txt` contains `0.0`.