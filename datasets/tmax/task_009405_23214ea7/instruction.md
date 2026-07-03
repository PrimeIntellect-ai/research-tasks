You are an ML engineer preparing a spatial dataset for training a surrogate model. You have a high-resolution 2D feature field stored as a 256x256 matrix of comma-separated floats in `/home/user/field_data.csv`. 

To speed up training without losing critical physical information, you need to determine the optimal grid coarsening step. You want to subsample the grid by taking every $k$-th point along both rows and columns (i.e., `A[::k, ::k]` in Python/NumPy notation) for $k \in \{1, 2, 4, 8, 16\}$. 

To evaluate the information loss (convergence testing), you will monitor the dominant spectral feature: the largest singular value of the matrix. Because subsampling reduces the matrix size and energy, you must scale the largest singular value of the subsampled matrix by $k$ to compare it to the original domain's magnitude. 

Your tasks:
1. Load `/home/user/field_data.csv` as a 2D array.
2. For each $k \in \{1, 2, 4, 8, 16\}$, extract the subsampled matrix and compute its largest singular value using Singular Value Decomposition (SVD).
3. Compute the scaled singular value: $\sigma_{scaled}(k) = \sigma_1(k) \times k$.
4. Calculate the relative error against the full-resolution baseline ($k=1$): 
   $Error = \frac{|\sigma_{scaled}(k) - \sigma_{scaled}(1)|}{\sigma_{scaled}(1)}$
5. Find the maximum $k$ from the set $\{1, 2, 4, 8, 16\}$ that yields a relative error strictly less than **0.05**.

Write the result to `/home/user/optimal_k.txt`. The file should contain exactly one line with the optimal $k$ and its corresponding scaled largest singular value, separated by a comma. Round the singular value to exactly 4 decimal places.
Format example: `4,123.4567`