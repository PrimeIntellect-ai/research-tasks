You are a performance engineer tasked with debugging and running a structural bioinformatics pipeline. 

The pipeline simulates the steady-state distribution of a biochemical signal across a protein-protein interaction network. The governing equation for the steady state is:
$M \vec{c} = \vec{S}$

Where:
- $\vec{c}$ is the concentration vector we want to find.
- $\vec{S}$ is the source vector.
- $M = (L - 2I)^2$, where $L$ is the unnormalized graph Laplacian ($L = D - A$) of the interaction network, and $I$ is the identity matrix.

**The Problem:**
The matrix $M$ is mathematically near-singular (and highly ill-conditioned). The previous implementation used standard LU factorization and crashed. You need to write a new script in any language of your choice that robustly computes the solution using the Moore-Penrose pseudo-inverse (e.g., using SVD with a standard cutoff threshold like $10^{-15}$ for singular values).

**Inputs (already existing on your system):**
1. `/home/user/network.csv`: The edge list of the undirected interaction graph. Format: `NodeA,NodeB` (one edge per line).
2. `/home/user/source.csv`: The source vector $\vec{S}$. Format: `Node,Value`.
3. `/home/user/sequences.fasta`: DNA sequences associated with each protein node.

**Instructions:**
1. Construct the Laplacian $L$ and the matrix $M$. **Crucial:** Ensure the rows and columns of your matrices strictly follow the alphabetical sorting of the node names (e.g., P00, P01, P02...).
2. Construct the source vector $\vec{S}$ matching the same alphabetical node order.
3. Solve $M \vec{c} = \vec{S}$ for $\vec{c}$ using the pseudo-inverse.
4. Identify the top two nodes with the *highest* (maximum) concentration values in $\vec{c}$.
5. Extract the DNA sequences for these two nodes from the FASTA file.
6. Compute the Longest Common Substring (LCS) between these two sequences. This represents a shared "primer" binding region.
7. Output your final results to `/home/user/report.json` using exactly this format (round concentration values to exactly 5 decimal places):

```json
{
    "top_node_1": "P_Highest",
    "top_node_1_c": 0.12345,
    "top_node_2": "P_SecondHighest",
    "top_node_2_c": 0.01234,
    "primer_lcs": "AGCT..."
}
```