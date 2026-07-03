You are a researcher modeling signal diffusion on a protein structure. You need to write a script to perform the following analysis:

1. Read the PDB file `/home/user/structure.pdb` and extract the 3D coordinates of all C-alpha (`CA`) atoms in the order they appear.
2. Build an unweighted undirected graph where each node is a CA atom. An edge exists between two nodes if the Euclidean distance between them is strictly less than 6.0 Angstroms.
3. Construct the graph Laplacian matrix $L = D - A$, where $A$ is the adjacency matrix and $D$ is the diagonal degree matrix.
4. Model a diffusion process on this graph defined by the ODE: $\frac{d\mathbf{u}}{dt} = -0.05 L \mathbf{u}$.
5. Consider the set of candidate source atoms to be the first 5 CA atoms (0-based indices 0, 1, 2, 3, 4). You need to find which of these source atoms, if given an initial concentration of $u_i(0) = 1.0$ (with all other atoms $u_j(0) = 0$), maximizes the concentration at the **last** CA atom in the PDB file at time $t = 20.0$.
6. Output your final result to `/home/user/result.txt` exactly in this format: `Index: X, Concentration: Y` where `X` is the 0-based index of the optimal source atom, and `Y` is the maximum concentration rounded to 6 decimal places.

You may use any programming language. Do not modify the PDB file.