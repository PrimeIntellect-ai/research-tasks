You are an AI assistant helping a structural bio-data scientist analyze the spatial distribution of protein residues. You will need to write Python code to parse structural files, perform array manipulations to calculate physical properties, fit statistical models to the data, visualize the results, and write regression tests to ensure the analysis code is robust.

Your task is to implement an end-to-end pipeline in Python.

**1. Setup & Environment:**
* Ensure your environment has the necessary libraries. You may use `numpy`, `scipy`, `matplotlib`, `biopython`, and `pytest`. 
* All your work should be done in `/home/user/`.
* The input files are located at `/home/user/input/protein.pdb` and `/home/user/input/protein.fasta`.

**2. Data Parsing & Processing (`/home/user/protein_analysis.py`):**
Write a script that does the following:
* **Parsing:** Read `protein.fasta` and count the number of amino acids. Read `protein.pdb` and extract the coordinates of all Alpha-Carbon (`CA`) atoms. Ensure the number of `CA` atoms exactly matches the FASTA sequence length. If not, raise a `ValueError`.
* **Array Manipulation:** Using `numpy`, calculate the Center of Mass (CoM) of the `CA` atoms (assume all `CA` atoms have equal weight). Then, calculate the Euclidean distance of each `CA` atom from the CoM.
* **Density Estimation:** Fit a Gamma distribution to the calculated distances using `scipy.stats.gamma.fit()`. 
* **Output Parameters:** Save the fitted parameters to a JSON file at `/home/user/output/gamma_params.json` with the exact keys: `{"a": float, "loc": float, "scale": float}`.
* **Visualization:** Generate a plot saving it to `/home/user/output/distance_distribution.png`. The plot must contain a histogram of the distances (density=True) and an overlay of the fitted Gamma Probability Density Function (PDF).

**3. Regression Testing (`/home/user/test_protein_analysis.py`):**
The scientist wants to make sure future changes to the distance calculation and fitting logic do not break the model.
* Write a `pytest` test file.
* Include a test `test_distance_computation()` that provides a small, hardcoded 3x3 numpy array of coordinates (e.g., `[[0,0,0], [2,0,0], [0,2,0]]`), computes the CoM and distances using your functions, and asserts the distances match the mathematically expected values using `np.testing.assert_allclose`.
* Include a test `test_gamma_fit()` that passes an array of dummy distances `[1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 4.0, 5.0]`, fits the Gamma distribution, and asserts the `a` (shape) parameter is strictly greater than 0.

**Execution:**
Run your analysis script to generate the JSON and PNG outputs, and then run `pytest /home/user/test_protein_analysis.py` to ensure your tests pass.