You are a data scientist working on structural bioinformatics. You need to fit models to the spatial distribution of specific amino acids within a protein structure to test a biophysical hypothesis.

You have been provided with a synthetic protein structure file at `/home/user/protein.pdb`. 

Your task is to analyze the spatial distribution of Alanine (ALA) residues and compare it to a theoretical null model. Follow these precise steps:

1. **Parse the PDB file**: Extract the 3D coordinates (x, y, z) of all Alpha-Carbon atoms. In the PDB file, these are the atoms where the atom name is exactly `CA`.
2. **Calculate the Center of Mass (CoM)**: Compute the center of mass of the protein using *all* `CA` atoms. Assume all `CA` atoms have equal mass (i.e., just compute the mean of the x, y, and z coordinates respectively).
3. **Extract Alanine Distances**: Find all `CA` atoms that belong to Alanine residues (residue name `ALA`). Calculate the Euclidean distance from the protein's CoM to each of these ALA `CA` atoms. This is your empirical distance distribution.
4. **Hypothesis Testing**: We hypothesize that the distance of ALA residues from the CoM follows a Rayleigh distribution with a scale parameter ($\sigma$) of 15.0. 
   - Perform a one-sample Kolmogorov-Smirnov (KS) test to compare your empirical ALA distances against the theoretical Rayleigh distribution (where loc=0 and scale=15.0).
5. **Distribution Distance Metric**: Calculate the 1D Wasserstein distance between your empirical ALA distances and a theoretical sample. To ensure reproducibility, generate the theoretical sample in Python using NumPy exactly like this: `numpy.random.default_rng(42).rayleigh(scale=15.0, size=100000)`.

**Output Specification:**
Create a JSON file at `/home/user/results.json` containing the results of your analysis. All floating-point numbers must be rounded to exactly 4 decimal places. The JSON must have the following exact keys:
- `"com_x"`: The x-coordinate of the Center of Mass.
- `"com_y"`: The y-coordinate of the Center of Mass.
- `"com_z"`: The z-coordinate of the Center of Mass.
- `"wasserstein_distance"`: The calculated Wasserstein distance.
- `"ks_statistic"`: The test statistic from the KS test.
- `"ks_pvalue"`: The p-value from the KS test.

You may write and execute any Python scripts you need in `/home/user/`.