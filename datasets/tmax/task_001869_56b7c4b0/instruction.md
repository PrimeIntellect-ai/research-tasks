As a bioinformatics analyst, you need to reconstruct a sequence analysis pipeline using a legacy embedding tool. 

Located at `/app/seq_embedder` is a stripped compiled binary that takes a standard FASTA file as input and outputs a raw 32-bit float binary file containing the numerical embeddings of the sequences (shape: `N x 64`, where N is the number of sequences). 

Your task is to build a Python-based scientific pipeline that does the following:
1. Run `/app/seq_embedder` on the provided training sequences at `/home/user/data/train.fasta`.
2. Load the resulting 64-dimensional sequence embeddings.
3. Use Singular Value Decomposition (SVD) to project these embeddings down to the top 3 principal components.
4. Fit a 2-component Gaussian Mixture Model (GMM) to this 3D projected data (density estimation).
5. Create a regression/evaluation script at `/home/user/evaluate.py` that takes a FASTA file path as a command-line argument, processes it through the binary, applies the *exact same* SVD projection learned from the training set, computes the Mean Log-Likelihood (MLL) of the test samples under the fitted GMM, and prints only this single float value to standard output.

Constraints:
- You must write the solution in Python. You may use `numpy`, `scipy`, and `scikit-learn`.
- The evaluation script must handle the end-to-end process (invoking the binary, reading the float32 output, projecting, and scoring).
- Output *only* the float value representing the MLL in the final `evaluate.py` standard output.

Ensure your analytical solution properly stores the projection matrix and GMM parameters so they can be applied to unseen data.