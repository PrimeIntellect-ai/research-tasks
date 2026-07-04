You are an ML engineer preparing baseline training data for a sequence binding affinity model. You have a raw dataset of DNA sequences and their corresponding continuous target values.

Your task is to create a Python script that processes this data and finds optimal linear weights for the top latent features of the sequences. 

Perform the following steps exactly as described:
1. Read the dataset from `/home/user/data.csv`. The file has columns `id`, `sequence`, and `target`.
2. Compute the 2-mer (dinucleotide) frequency vector for each sequence. Count overlapping 2-mers. Sort the 16 possible 2-mers alphabetically (AA, AC, AG, AT, CA, ..., TT). This yields an $N \times 16$ feature matrix $M$.
3. Perform Singular Value Decomposition (SVD) on $M$ such that $M = U \Sigma V^T$. Project the data onto the first 2 principal components by computing $X = U[:, :2] \times \text{diag}(\Sigma[:2])$. (Use `scipy.linalg.svd` with `full_matrices=False`).
4. Using `scipy.optimize.minimize` (with the default BFGS algorithm), find the 2-dimensional weight vector $w$ that minimizes the Mean Squared Error: $\frac{1}{N} \sum_{i=1}^N (X_i \cdot w - y_i)^2$. Use an initial guess of $w = [0.0, 0.0]$.
5. Save the optimized weights $w_0$ and $w_1$ as comma-separated floats (rounded to 4 decimal places) in `/home/user/solution.txt` (e.g., `1.2345,-0.6789`).

You may need to create a virtual environment or install dependencies (`numpy`, `pandas`, `scipy`) using pip.