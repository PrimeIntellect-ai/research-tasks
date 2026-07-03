You are a machine learning engineer preparing graph-based features from protein structures to train a new geometric deep learning model. 

We need to establish an automated, reproducible workflow that extracts the spectral embedding of a protein's residue-interaction graph directly from its spatial coordinates.

Your task is to write a Jupyter Notebook that processes a PDB file and extracts these features, and then orchestrate its execution headlessly via the terminal.

**Requirements:**
1. A protein structure file is located at `/home/user/workspace/input.pdb`.
2. Create a Jupyter Notebook named `/home/user/workspace/extract_features.ipynb` that performs the following steps when executed:
   - Parse the PDB file and extract the 3D coordinates (X, Y, Z) of all Alpha Carbon atoms (where the atom name is exactly `CA`). Ignore all other atoms.
   - Calculate the pairwise Euclidean distance matrix $D$ between these CA atoms.
   - Construct an unweighted, undirected adjacency matrix $A$ representing the protein's interaction graph. Two residues (nodes) are connected ($A_{i,j} = 1$) if the distance between their CA atoms is strictly greater than 0 and less than or equal to 8.0 Ångstroms ($0 < D_{i,j} \le 8.0$). Otherwise, $A_{i,j} = 0$.
   - Compute the Singular Value Decomposition (SVD) of the adjacency matrix $A$.
   - Extract the top 5 largest singular values from the decomposition.
   - Save these 5 values, sorted in descending order, to a file named `/home/user/workspace/features.csv`. The file should contain exactly one line with the 5 values comma-separated, each rounded to exactly 4 decimal places (e.g., `5.1234,4.0000,2.1000,1.5550,0.1200`).
3. After creating the notebook, execute it headlessly from the command line in the `/home/user/workspace/` directory so that it fully runs from start to finish and generates `features.csv`. You may use `jupyter nbconvert` or any standard notebook runner available in the environment.

Ensure your notebook contains all necessary imports and handles the parsing and math correctly.