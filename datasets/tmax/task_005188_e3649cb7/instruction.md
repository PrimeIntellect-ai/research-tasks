You are a data scientist working on a structural bioinformatics project. Your colleague wrote a Python script (`/home/user/scripts/analyze.py`) to analyze a protein structure (`/home/user/data/protein.pdb`). 

The script is supposed to:
1. Parse the C-alpha atoms from the PDB file.
2. Build a contact graph (edges where Euclidean distance < 7.0 Å).
3. Compute the degree centrality of each node.
4. Regress the degree centrality against structural features.

However, the script crashes or produces wildly unstable results because the feature matrix $X$ is near-singular (it contains a perfectly collinear synthetic feature). 

Your task is to:
1. Create a Python virtual environment at `/home/user/venv` and install the necessary dependencies (`numpy`, `biopython`, `networkx`, `scikit-learn`).
2. Fix the script `/home/user/scripts/analyze.py`. Remove the buggy Ordinary Least Squares (`np.linalg.inv(...)`) implementation and replace it with L2-regularized Ridge regression using `sklearn.linear_model.Ridge`. 
   - You must use `alpha=1.0`.
   - You must set `fit_intercept=False` (since the bias column is already explicitly included in the feature matrix $X$).
3. Run the script so that it successfully outputs the model coefficients to `/home/user/results/coefficients.txt`. The script is already set up to write each coefficient on a new line, formatted to 4 decimal places.

Ensure the final output file `/home/user/results/coefficients.txt` exists and contains the correct 3 coefficients.