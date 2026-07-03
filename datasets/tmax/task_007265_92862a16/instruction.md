You are an AI assistant acting as a bioinformatics analyst. Your objective is to model the interaction dynamics of a set of genetic sequences using their k-mer similarities, simulate their expression over time, and compare the final state to a uniform baseline. 

Perform the following steps:

1. **Environment Setup**
   Create a Python virtual environment at `/home/user/sim_env` and install `numpy` and `scipy`. All your scripts should use the Python interpreter from this virtual environment.

2. **Input Data**
   Create a FASTA file at `/home/user/data/sequences.fasta` (you will need to create the directory) containing the following exact sequences:
   ```text
   >Seq1
   ATGCATGCAT
   >Seq2
   GCATGCATGC
   >Seq3
   CGATCGATCG
   >Seq4
   ATATATATAT
   >Seq5
   CGCGCGCGCG
   ```

3. **Matrix Construction**
   Write a Python script that reads the FASTA file and computes a 2-mer frequency vector for each sequence. The 2-mers should be constructed from the alphabet A, C, G, T and ordered lexicographically (AA, AC, AG, AT, CA, ..., TT). 
   Construct a $5 \times 5$ interaction matrix $M$ where $M_{i,j}$ is the standard dot product of the 2-mer frequency vectors of sequence $i$ and sequence $j$.

4. **Matrix Decomposition**
   Perform Singular Value Decomposition (SVD) on $M$. Reconstruct a smoothed interaction matrix $\tilde{M}$ using only the top 2 singular values (i.e., zero out the remaining singular values and multiply the matrices back together).

5. **ODE Simulation**
   Use $\tilde{M}$ to simulate a system of ordinary differential equations (ODEs) representing gene expression dynamics:
   $$\frac{dx}{dt} = 0.05 \tilde{M} x - 0.1 x$$
   Where $x$ is a column vector of size 5. The initial condition at $t=0$ is $x(0) = [1.0, 0.0, 0.0, 0.0, 0.0]^T$.
   Solve this ODE from $t=0$ to $t=10$ using `scipy.integrate.solve_ivp` with the default 'RK45' method.

6. **Probability Distance**
   Extract the final state vector $x(10)$. Convert this vector into a probability distribution $P$ using the softmax function: $P_i = \frac{e^{x_i}}{\sum_{j} e^{x_j}}$.
   Compute the Jensen-Shannon distance (using `scipy.spatial.distance.jensenshannon` with base $e$) between $P$ and a uniform probability distribution $Q = [0.2, 0.2, 0.2, 0.2, 0.2]$.

7. **Output**
   Save your final results to a JSON file at `/home/user/analysis_output.json` with the following format (round the floats to 4 decimal places):
   ```json
   {
     "top_singular_value": 0.0000,
     "js_distance": 0.0000
   }
   ```