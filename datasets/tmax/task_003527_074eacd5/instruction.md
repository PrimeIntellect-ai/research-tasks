You are a data scientist analyzing the geometric properties of a protein structure. You need to build a reproducible computation pipeline that extracts structural features from a PDB (Protein Data Bank) file, applies matrix decomposition to find its principal axes, and is orchestrated entirely within a Jupyter Notebook.

Here are your instructions:

1. You will find a PDB file at `/home/user/protein.pdb`. (Assume it is already there).
2. Create a Jupyter Notebook named `/home/user/analyze_structure.ipynb` that performs the following steps when executed:
   a. Parses `/home/user/protein.pdb` to extract the 3D coordinates (X, Y, Z) of all Alpha-Carbon atoms. In a standard PDB file, these are lines starting with `ATOM`, where the atom name (characters 13-16, 1-indexed) is exactly ` CA ` (C-alpha).
   b. Constructs an $N \times 3$ NumPy matrix of these coordinates (where $N$ is the number of CA atoms) in the order they appear.
   c. Mean-centers this coordinate matrix (subtract the mean of each column from the respective column so the centroid is at the origin).
   d. Performs Singular Value Decomposition (SVD) on the mean-centered coordinate matrix.
   e. Writes the resulting singular values to a text file located at `/home/user/singular_values.txt`. The file should contain one singular value per line, sorted in descending order, and each value must be rounded to exactly 4 decimal places (e.g., `3.1416`).
3. Install any necessary Python packages to run and orchestrate your notebook.
4. Execute your notebook headlessly from the command line (e.g., using `jupyter nbconvert --execute`) so that it generates the `/home/user/singular_values.txt` file.

Make sure your notebook is robust and completely self-contained. The final verification will check the existence and contents of `/home/user/singular_values.txt`, as well as the presence of the `/home/user/analyze_structure.ipynb` notebook.