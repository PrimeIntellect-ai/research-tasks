You are an AI assistant helping a computational physicist analyze the results of a coupled oscillator simulation.

The researcher has simulated a network of 100 oscillators. You have been provided with two files:
1. `/home/user/network_topology.txt`: An edge list representing the physical connections between oscillators (nodes are 0-indexed integers). Format: `u v` per line.
2. `/home/user/simulation_data.npy`: A 2D NumPy array of shape `(100, 1000)` containing the time-series displacements of the 100 oscillators over 1000 time steps. The sampling interval is `dt = 0.01` seconds (i.e., the sampling frequency is 100 Hz).

Your goal is to identify the largest "synchronization cluster" in the network. A synchronization cluster is defined as a connected component in the network where all connected oscillators share the same dominant frequency.

Please perform the following steps:
1. Set up a Python virtual environment at `/home/user/venv` and install any necessary scientific packages (e.g., `numpy`, `networkx`, `scipy`).
2. Load the time-series data.
3. For each oscillator, compute its dominant frequency using a Discrete Fourier Transform. The dominant frequency is the frequency corresponding to the maximum magnitude in the amplitude spectrum. **Ignore the DC component (0 Hz) when finding the maximum.**
4. Filter the original network topology to create a new undirected graph: an edge between node `u` and node `v` should only exist if they were connected in the original topology AND their dominant frequencies are extremely close: `abs(f_u - f_v) <= 0.1` Hz.
5. Find the largest connected component in this frequency-filtered graph.
6. Write the node IDs of the oscillators in this largest connected component to a file named `/home/user/largest_sync_cluster.txt`. The IDs must be sorted in ascending order and separated by a single comma (e.g., `2,4,5,10...`). There should be no trailing comma and no spaces.

Make sure your final output file is exactly formatted as requested so the automated grading script can verify it.