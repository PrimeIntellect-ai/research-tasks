You are a data scientist tasked with fitting a linear model to biological sequence data. You have a matrix of features stored in an HDF5 file and a set of sequences in a FASTA file. Your goal is to extract the data, solve the linear system to find the model weights, and validate the solution analytically—all orchestrated via a single Bash script.

Write a Bash script at `/home/user/analyze.sh` that performs the following steps:

1. **Parse Bioinformatics Data**: Read the FASTA file `/home/user/seqs.fasta`. Calculate the sequence length for each sequence (ignoring the `>` header lines). These lengths form the target column vector `y` (in the order they appear in the file).

2. **Extract Scientific Data**: Use `h5dump` to extract the 2D matrix dataset named `/X` from the HDF5 file `/home/user/data.h5`.

3. **Matrix Decomposition / System Solving**: Use a Python one-liner (or short inline Python script) invoked from within your Bash script to solve the linear system `X * w = y` for the weight vector `w`. 

4. **Output Weights**: Write the resulting vector `w` to `/home/user/weights.txt`, with one numerical value per line (e.g., `10.0`).

5. **Analytical Validation**: Using only standard Bash text processing tools and math utilities (like `awk` and `bc`), calculate the L2 norm (Euclidean norm) of the vector `w`. Write the final norm to `/home/user/norm.txt`, rounded to exactly 2 decimal places.

**Constraints:**
- Your solution must be fully contained within `/home/user/analyze.sh`.
- The script must be executable (`chmod +x`).
- Do not hardcode the sequence lengths or matrix values; your script must dynamically read from the provided files.