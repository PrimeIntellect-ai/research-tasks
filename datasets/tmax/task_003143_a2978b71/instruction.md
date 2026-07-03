You are a performance engineer analyzing a structural bioinformatics application. The application models protein dynamics using the Gaussian Network Model (GNM), which reduces the protein to a network of alpha-carbon (CA) atoms. The original application crashes due to a "Singular Matrix" error when solving the steady-state equations because the Laplacian (Kirchhoff) matrix of the protein network has a zero eigenvalue (corresponding to translational invariance). 

Your task is to implement a robust Python script to calculate the difference in global flexibility between two protein conformations provided as PDB files. 

Follow these steps:
1. Two PDB files are located at `/home/user/state1.pdb` and `/home/user/state2.pdb`.
2. Write a Python script (e.g., `/home/user/analyze.py`) that parses these PDB files.
3. For each file, extract the 3D coordinates of all atoms named exactly `CA`.
4. Construct the Kirchhoff (Laplacian) matrix $\Gamma$ for each state. The matrix is defined as:
   - Off-diagonal element $\Gamma_{ij} = -1$ if the Euclidean distance between atom $i$ and atom $j$ is $\le 8.0$ Å, and $0$ otherwise.
   - Diagonal element $\Gamma_{ii} = -\sum_{j \ne i} \Gamma_{ij}$ (so that the sum of each row is 0).
5. To avoid the singular matrix issue, compute the Moore-Penrose pseudo-inverse of the Kirchhoff matrix, $\Gamma^{+}$.
6. Calculate the total mean square fluctuation for each state, which is simply the trace (sum of diagonal elements) of $\Gamma^{+}$.
7. Calculate the absolute difference between the trace of $\Gamma^{+}$ for `state1.pdb` and `state2.pdb`.
8. Write this absolute difference as a float, rounded to exactly 4 decimal places, to the file `/home/user/fluctuation_diff.txt`.

Ensure your script handles the file parsing and mathematical operations correctly. You may use `numpy` and `scipy`.