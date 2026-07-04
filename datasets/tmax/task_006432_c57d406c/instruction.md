You are acting as a bioinformatics analyst. We need to establish a theoretical "random coil" baseline for a specific human protein sequence before we run expensive molecular dynamics simulations. We will use a Monte Carlo 3D lattice random walk model and compare it to analytical polymer physics.

Your task is to write and execute a Python script at `/home/user/run_analysis.py` that performs the following steps:

1. **Parse the Sequence:** Read the FASTA file located at `/home/user/protein.fasta` (you will need to install any required packages, like `biopython`). Determine the length of the amino acid sequence, let's call it `N`.
2. **Monte Carlo Simulation:** Model the protein backbone as a freely jointed chain on a 3D cubic lattice. Simulate 10,000 independent random walks. Each walk should start at the origin (0,0,0) and take `N-1` steps. Each step must be exactly length 1, randomly choosing one of the 6 adjacent lattice points (i.e., $\pm1$ in the X, Y, or Z direction).
3. **Analytical Validation:** Calculate the Monte Carlo mean squared end-to-end distance, $\langle R^2_{MC} \rangle$, across all 10,000 simulations. Compare this to the theoretical expected mean squared distance for a random walk, which is $\langle R^2_{analytical} \rangle = N - 1$.
4. **Export Results:** Save a JSON file at `/home/user/analysis.json` with the exact following keys:
   - `"sequence_length"`: (integer) The length of the parsed protein sequence `N`.
   - `"mc_mean_squared_distance"`: (float) The calculated $\langle R^2 \rangle$ from your Monte Carlo simulations.
   - `"analytical_mean_squared_distance"`: (integer) The theoretical $\langle R^2 \rangle$.
   - `"relative_error"`: (float) Calculated as `abs(mc - analytical) / analytical`.
5. **Visualization:** Create a histogram of the end-to-end distances (not squared) from your 10,000 simulations. Save this plot as `/home/user/distance_distribution.png`.

Please write the code, install any necessary dependencies, and run your script to produce the output files. Ensure your outputs exactly match the requested paths and JSON keys.