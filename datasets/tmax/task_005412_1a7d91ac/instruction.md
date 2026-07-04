I am working on a structural bioinformatics pipeline in Rust to analyze protein residue contact networks, but my model fitting code is failing.

I have a Cargo project at `/home/user/protein_network`. It reads a PDB (Protein Data Bank) file, extracts the C-alpha (CA) atoms, builds a contact graph (edges exist if the Euclidean distance between two CA atoms is $\le 8.0$ Å), and tries to compute the eigenvector centrality (dominant eigenvector) of the network using power iteration to identify the most structurally critical residues.

There are two major problems:
1. **Performance:** The pairwise distance calculation is extremely slow for larger proteins. It currently uses standard sequential loops.
2. **Numerical Instability:** The power iteration is failing to converge on certain inputs. This happens because the contact graph of my multimeric protein has bipartite or disconnected structures, causing the transition matrix to be near-singular or have alternating eigenvalues, which makes the standard power iteration oscillate infinitely.

Your task:
1. Modify `/home/user/protein_network/src/main.rs` to parallelize the pairwise distance matrix computation. Use the `rayon` crate (you will need to add it to the project).
2. Fix the numerical instability in the power iteration. Implement a PageRank-style damping factor of `0.85` to stabilize the iteration and properly handle disconnected or bipartite components. The modified iteration step should be $v_{t+1} = 0.85 \cdot M v_t + \frac{0.15}{N} \mathbf{1}$, where $M$ is the column-stochastic transition matrix of the contact graph, $N$ is the number of nodes, and $\mathbf{1}$ is a vector of ones. Run the iteration for 100 steps.
3. The program currently takes the input PDB file path as its first command-line argument. Run your fixed program on the provided file `/home/user/data/complex.pdb`.
4. Create a file at `/home/user/top_residues.txt` containing the Chain Identifier and Residue Sequence Number of the top 3 residues with the highest centrality scores, sorted in descending order of their score. Format each line as `Chain:ResNum` (e.g., `A:42`). If there's a tie, sort alphabetically by Chain, then numerically by ResNum.

Ensure your code compiles and runs successfully. You do not need to alter the PDB parser if it correctly parses CA atoms.