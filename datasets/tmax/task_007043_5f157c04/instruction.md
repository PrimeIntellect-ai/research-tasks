You are a Machine Learning Engineer preparing protein sequence and structure data for a new generative model. Before training, you need to extract some baseline statistical properties from your raw data.

Your data is located in `/home/user/data/`:
1. `/home/user/data/input.fasta`: Contains protein sequences.
2. `/home/user/data/protein.pdb`: Contains 3D structural coordinates and metadata.

Write a Python script `/home/user/process_data.py` to perform the following analysis:

1. **FASTA Parsing & Bootstrap CI:** Read `input.fasta` and extract the lengths of all sequences. Calculate the 95% bootstrap confidence interval for the mean of these sequence lengths. 
   * Constraint: You must use `scipy.stats.bootstrap` with `confidence_level=0.95`, `n_resamples=1000`, `method='percentile'`, and `random_state=42`. Pass the lengths as a 1D numpy array.

2. **PDB Parsing & Distribution Fitting:** Read `protein.pdb` and extract the B-factor values specifically for all Alpha-Carbon atoms (atom name `CA`). Fit a Normal distribution to these extracted B-factor values using `scipy.stats.norm.fit`.

3. **Output:** Save your results to a JSON file at `/home/user/metrics.json` with the following exact keys:
   * `"seq_len_ci_low"`: Lower bound of the bootstrap CI (float).
   * `"seq_len_ci_high"`: Upper bound of the bootstrap CI (float).
   * `"bfactor_norm_loc"`: The fitted mean (loc) of the Normal distribution (float).
   * `"bfactor_norm_scale"`: The fitted standard deviation (scale) of the Normal distribution (float).

Round all float values in the JSON output to exactly 4 decimal places.
You may install any required Python packages (e.g., `biopython`, `scipy`) using `pip`.