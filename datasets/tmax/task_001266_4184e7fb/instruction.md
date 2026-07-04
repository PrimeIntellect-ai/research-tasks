You are a performance engineer assisting a bioinformatics team. They have a script `/home/user/motif_nmf.py` that processes a matrix of k-mer frequencies from designed primers using Non-negative Matrix Factorization (NMF). 

However, they are experiencing two major problems:
1. **Performance:** The script is incredibly slow. The original author used naive nested loops for the matrix updates instead of utilizing multi-dimensional array operations.
2. **Stability:** The k-mer matrix (`/home/user/kmer_matrix.npy`) contains near-singular structures (highly identical sequence profiles). The current NMF implementation crashes with a `RuntimeWarning: invalid value encountered in true_divide` and produces matrices full of `NaN`s because the denominator in the update rule approaches zero.

Your task is to fix and extend the pipeline:

1. **Optimize and Fix the Code:**
   - Modify `/home/user/motif_nmf.py`.
   - Replace the nested loops in the NMF update step with fully vectorized NumPy operations.
   - Fix the numerical instability by adding a small constant ($\epsilon = 10^{-9}$) to the denominator of the NMF multiplicative update rules.
   - Maintain the existing `np.random.seed(42)` initialization and the 50 iterations limit.

2. **Data Visualization:**
   - Extend `/home/user/motif_nmf.py` to generate a heatmap of the resulting `W` matrix using `matplotlib`.
   - Save the visualization to `/home/user/W_heatmap.png`.
   - The script must also save the final matrices to `/home/user/W_out.npy` and `/home/user/H_out.npy` (this part is already partially in the boilerplate, ensure it works).

3. **Reproducible Pipeline:**
   - Create a `requirements.txt` file in `/home/user/` containing the necessary Python packages.
   - Create a bash script `/home/user/run.sh` that:
     a) Creates a Python virtual environment at `/home/user/.venv`.
     b) Activates it.
     c) Installs the dependencies from `requirements.txt`.
     d) Runs `motif_nmf.py`.
   - Ensure `run.sh` is executable.

You must not change the shape of the inputs or the mathematical intent of the multiplicative NMF, only its implementation efficiency and stability.