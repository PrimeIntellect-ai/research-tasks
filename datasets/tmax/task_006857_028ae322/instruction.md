You are a bioinformatics analyst troubleshooting a sequence analysis pipeline. We have a set of DNA sequences and we need to calculate the rolling GC-content variance across them. A previous pipeline produced unstable variance results due to floating-point precision issues in a naive variance formula. 

Your task is to:
1. Parse the FASTA file located at `/home/user/sequences.fasta`.
2. For each window size $W \in \{10, 20, 30, ..., 100\}$:
   a. For each sequence, calculate the GC-content fraction (number of G or C bases / $W$) for all possible contiguous sliding windows of size $W$ (step size = 1).
   b. Aggregate all GC-content fractions from all windows across ALL sequences into a single collection.
   c. Compute the population variance of these GC-content fractions using a numerically stable method (e.g., `numpy.var` with `ddof=0` uses a stable algorithm).
3. Compare your computed variances against the reference values in `/home/user/reference_variances.csv` (which contains `WindowSize,ReferenceVariance`). Calculate the absolute difference for each $W$.
4. Perform convergence testing: find the smallest window size $W$ where the absolute difference between your calculated variance and the reference variance is strictly less than $1 \times 10^{-6}$.
5. Orchestrate this workflow by creating a Jupyter Notebook at `/home/user/analysis.ipynb`. The notebook must:
   - Perform all the calculations described above.
   - Generate a plot comparing your computed variance and the reference variance against $W$, and save it as `/home/user/variance_comparison.png`.
   - Write the smallest converged window size $W$ (as a simple integer) to `/home/user/converged_W.txt`.
6. Execute the notebook headlessly. You can use `jupyter nbconvert --to notebook --execute /home/user/analysis.ipynb`.

Ensure all necessary packages (like `jupyter`, `numpy`, `pandas`, `matplotlib`, `biopython`) are installed in your environment if you need them.