You are acting as a bioinformatics analyst. Your task is to process a set of DNA sequences, perform dimensionality reduction, solve a classification problem linearly, and conduct a statistical hypothesis test, all orchestrated within a Jupyter Notebook.

We have placed a FASTA file at `/home/user/sequences.fasta`. The file contains 50 DNA sequences. The headers indicate the group each sequence belongs to, either `>GroupA_seqX` or `>GroupB_seqX`.

Please perform the following steps by creating a Jupyter Notebook at `/home/user/analysis.ipynb`:

1. **K-mer extraction**: Read `/home/user/sequences.fasta` and compute the normalized 3-mer (trimer) frequencies for each sequence. There are 64 possible 3-mers. Sort them in standard alphabetical order (AAA, AAC, AAG, AAT, CAA, ..., TTT). The frequency is the raw count divided by the total number of 3-mers in that sequence (which is length - 2). Construct a feature matrix `X` of size $50 \times 64$ where rows correspond to the sequences in the exact order they appear in the FASTA file.
2. **Matrix decomposition**: Perform Singular Value Decomposition (SVD) on the uncentered matrix `X`. Use `X = U @ np.diag(S) @ Vt` (where SVD returns S as a 1D array of singular values in descending order). Project `X` onto its top 5 principal components: `X_reduced = U[:, :5] * S[:5]`.
3. **Linear Equation Solving**: Create a label vector `y` of size 50, where `y_i = 1` if the $i$-th sequence is in Group A, and `y_i = -1` if it is in Group B. Solve the linear system $(X_{reduced}^T X_{reduced}) w = X_{reduced}^T y$ to find the weight vector `w` (length 5). You can use a standard linear solver or least-squares function.
4. **Hypothesis comparison**: Compute the projected scores for all sequences: `s = X_reduced @ w`. Separate these scores into two arrays, one for Group A and one for Group B. Perform an independent two-sample t-test (assuming equal variance) comparing the scores of Group A and Group B.
5. **Output**: Your notebook must calculate these values and write a JSON file to `/home/user/results.json` containing the following structure:
```json
{
  "sum_top_5_singular_values": <float>,
  "w_0": <float>,
  "p_value": <float>
}
```
`w_0` is the first element of the weight vector `w`. Use 6 significant digits for the floats, or standard Python float serialization.

Once your notebook is ready, orchestrate the execution by running it headlessly from the terminal using `jupyter nbconvert --to notebook --execute /home/user/analysis.ipynb`.

Ensure `/home/user/results.json` is accurately produced and formatted correctly!