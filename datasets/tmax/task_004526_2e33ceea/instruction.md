You are a bioinformatics analyst tasked with evaluating the structural stability of a newly sequenced protein variant. To do this, you will need to fix and use a vendored third-party Python package, parse structural data, run a Monte Carlo simulation to generate conformational ensembles, and perform a statistical hypothesis test.

Here are the specific steps you must follow:

1. **Fix and Install the Vendored Package:**
   There is a vendored package located at `/app/vendored/struct-stats-1.1.0`. It is a specialized tool for calculating statistical distributions of protein metrics. However, its installation is currently broken due to an intentional perturbation in its configuration. Identify the issue preventing its installation via `pip`, fix it, and install the package into your Python environment.

2. **Parse the Protein Data:**
   You have been provided a reference structure at `/home/user/data/reference.pdb`. Write a Python script (`/home/user/analyze.py`) that parses this PDB file and extracts the 3D coordinates (x, y, z) of all Alpha-Carbon (`CA`) atoms.

3. **Monte Carlo Simulation:**
   Using the extracted `CA` coordinates as the starting state, simulate two distinct conformational ensembles representing a Wild-Type (WT) and a Mutant variant using a simple Monte Carlo random walk perturbation:
   - **WT Ensemble:** Generate 10,000 conformations. For each conformation, add independent Gaussian noise (mean = 0, standard deviation = 0.2 Å) to every `CA` coordinate.
   - **Mutant Ensemble:** Generate 10,000 conformations. For each conformation, add independent Gaussian noise (mean = 0, standard deviation = 0.5 Å) to every `CA` coordinate.
   *(Set the random seed to `42` using `numpy.random.seed(42)` before generating the noise for WT, and do not reset it between ensembles so the sequence of random numbers is deterministic).*

4. **Calculate Radius of Gyration:**
   For each conformation in both ensembles, calculate the Radius of Gyration ($R_g$). 
   $R_g = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (r_i - r_{mean})^2}$
   where $N$ is the number of `CA` atoms, $r_i$ is the coordinate vector of the $i$-th `CA` atom, and $r_{mean}$ is the centroid of the conformation's `CA` atoms.

5. **Statistical Hypothesis Comparison:**
   Use the `struct_stats.hypothesis` module from the package you installed to perform a permutation test comparing the $R_g$ distributions of the WT and Mutant ensembles. The function signature is `permutation_test(dist_a, dist_b, n_permutations=5000)`.
   
6. **Output:**
   Your script `/home/user/analyze.py` must write the final test statistic and p-value to a JSON file at `/home/user/results.json` in the following format:
   ```json
   {
       "test_statistic": 1.2345,
       "p_value": 0.001
   }
   ```

Ensure your script is self-contained and handles the entire pipeline (parsing, simulating, and testing) when run via `python3 /home/user/analyze.py`.