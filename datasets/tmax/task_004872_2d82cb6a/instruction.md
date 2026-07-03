You are an ML engineer preparing genomic training data. We are building a sequence representation model using a technique based on k-mer matrix factorization. 

You need to select an optimal blend of DNA primers to match a specific reference profile. To do this, you will use our custom library, `dna_factorize`.

However, there is a known issue: the vendored `dna_factorize` package fails and produces NaNs when given highly repetitive, near-singular input sequences. 

Here are your steps to complete the task:

1. **Fix the Vendored Package**: 
   The source code for `dna_factorize` version 1.2.0 is located at `/app/dna_factorize-1.2.0`. When performing its internal Non-negative Matrix Factorization (NMF) multiplicative update in `dna_factorize/core.py`, the denominator can become zero or dangerously close to zero for near-singular k-mer count matrices. 
   Find the update step for `H` (which looks like `denom = W.T @ X_reconstructed`) and add a small epsilon (`1e-9`) to the denominator to prevent division by zero. Reinstall the fixed package in your environment (e.g., `pip install -e /app/dna_factorize-1.2.0`).

2. **Embed the Primers**:
   You have a list of 100 candidate DNA primers in `/home/user/primers.txt` (one per line).
   Use the fixed package to extract their embeddings:
   ```python
   from dna_factorize import embed_sequences
   with open('/home/user/primers.txt') as f:
       primers = [line.strip() for line in f]
   embeddings = embed_sequences(primers) # returns a (100, 16) numpy array
   ```

3. **Optimization and Reference Comparison**:
   You are provided with a reference target profile at `/home/user/target_profile.npy` (shape `(16,)`).
   You must find a set of non-negative weights $w_i \ge 0$ for the 100 primers, such that $\sum_{i=1}^{100} w_i = 1$, which minimizes the Mean Squared Error (MSE) between the weighted average of the primer embeddings and the target profile.
   Let $E$ be the embeddings matrix. The prediction is $y = \sum w_i E_i$.
   The objective is to minimize $\frac{1}{16} \sum_{j=1}^{16} (y_j - \text{target}_j)^2$.

4. **Output Format**:
   Write your optimized weights to `/home/user/weights.csv`. 
   The file should contain a single line of 100 comma-separated floats representing the weights for the primers in the exact order they appear in `primers.txt`.

Your goal is to achieve an MSE of less than 0.005 against the target profile.