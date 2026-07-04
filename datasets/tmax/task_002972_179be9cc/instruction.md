You are a data analyst tasked with building a reproducible testing pipeline to verify the numerical accuracy of dimensionality reduction algorithms across multiple programming languages. Specifically, you will join data from multiple sources, perform Principal Component Analysis (PCA) in both Python and R, and mathematically verify that their outputs match despite language differences.

You are provided with three CSV files in your home directory:
- `/home/user/data_A.csv` (Contains `id`, `f1`, `f2`, `f3`)
- `/home/user/data_B.csv` (Contains `id`, `f4`, `f5`)
- `/home/user/data_C.csv` (Contains `id`, `f6`, `f7`, `f8`)

Perform the following steps:

1. **Multi-source Data Joining (Python):** 
   Write a Python script `/home/user/join_data.py` that reads the three CSV files, performs an inner join on the `id` column, and saves the combined dataset to `/home/user/joined_data.csv`. The output should be sorted by `id` ascending.

2. **Dimensionality Reduction (Python):**
   Write a Python script `/home/user/pca_py.py` using `pandas` and `scikit-learn` that reads `/home/user/joined_data.csv`. Excluding the `id` column, perform PCA to extract the top 2 principal components. Apply mean centering but NO variance scaling. Save the resulting scores to `/home/user/pca_python.csv` with exactly two columns named `PC1` and `PC2` (maintain the row order of the joined data).

3. **Dimensionality Reduction (R):**
   Write an R script `/home/user/pca_r.R` that reads `/home/user/joined_data.csv`. Using base R's `prcomp` function (with `center = TRUE` and `scale. = FALSE`), extract the top 2 principal components for the feature columns (excluding `id`). Save the scores to `/home/user/pca_r.csv` with exactly two columns named `PC1` and `PC2` (without row names).

4. **Numerical Accuracy Testing (Python):**
   Write a Python script `/home/user/test_accuracy.py` that loads `/home/user/pca_python.csv` and `/home/user/pca_r.csv`. Since PCA eigenvectors can be multiplied by -1 depending on the solver's initialization, take the absolute value of all PCA scores before comparing them. Calculate the maximum absolute difference between the absolute Python scores and the absolute R scores. 
   If the maximum absolute difference is strictly less than `1e-4`, write the word `PASS` to `/home/user/accuracy_report.txt`. Otherwise, write `FAIL`.

5. **Reproducible Pipeline:**
   Create a bash script `/home/user/run_pipeline.sh` that:
   - Installs any necessary Python packages (like `pandas` and `scikit-learn`) to the local user environment (do not use root/sudo). Base R already contains `prcomp`, so R package installation is not strictly necessary.
   - Runs `join_data.py`
   - Runs `pca_py.py`
   - Runs `pca_r.R`
   - Runs `test_accuracy.py`

Make sure your pipeline is fully reproducible. You can run `/home/user/run_pipeline.sh` yourself to verify it creates `/home/user/accuracy_report.txt` with the text `PASS`.