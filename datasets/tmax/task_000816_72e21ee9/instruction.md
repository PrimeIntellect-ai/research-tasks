You are acting as a bioinformatics software engineer. We have a set of high-dimensional deep learning embeddings representing viral genomic sequences, stored in an HDF5 file. We need to compute the pairwise attention log-scores between all sequences to identify clustering patterns.

The input data is located at: `/home/user/seq_data.h5`
Inside this file, there is a dataset named `embeddings` of shape `(N, M)` containing `float64` values, where `N` is the number of sequences and `M` is the embedding dimension.

Your task is to write and execute a Python script at `/home/user/compute.py` that does the following:
1. Reads the `embeddings` matrix $X$ from the input HDF5 file.
2. Computes the pairwise dot-product matrix $D$, where $D_{i,j} = X_i \cdot X_j$.
3. Computes the log-softmax of the dot products across each row to get the score matrix $S$. Mathematically, for each row $i$ and column $j$:
   $$S_{i,j} = \log\left(\frac{\exp(D_{i,j})}{\sum_{k=1}^N \exp(D_{i,k})}\right)$$
4. Saves the resulting $N \times N$ matrix $S$ to a new HDF5 file at `/home/user/results.h5` in a dataset named `log_scores` (as `float64`).

**Critical Constraints & Requirements:**
* **Numerical Stability:** The embedding dimensions and values are large enough that the dot products will easily exceed 700. A naive implementation of the formula above will cause `float64` overflow ($\exp(700) \approx \infty$), resulting in `NaN` values. You must implement or utilize a numerically stable approach for the log-softmax computation.
* **Parallel Computing:** You must parallelize the computation of the rows of $S$ using MPI (via the `mpi4py` library). Distribute the workload evenly across the MPI ranks.
* **Execution:** Once your script is written, you must install any necessary dependencies and run your script using exactly 4 MPI processes: `mpiexec -n 4 python /home/user/compute.py` (or `mpirun`).

If you need to install packages, use `pip`. Make sure your final output file `/home/user/results.h5` has exactly the correct values and no `NaN`s.