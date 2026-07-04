You are a Machine Learning Engineer preparing sequence data for a novel biophysics model. Your pipeline requires extracting structural features via numerical integration, calculating a sequence similarity covariance matrix using a custom C program, and decorrelating the features using a Cholesky decomposition written from scratch in AWK. 

You must accomplish the following tasks entirely using Bash, AWK, and standard Unix command-line tools.

**Phase 1: Compilation of Custom Alignment Scorer**
You have been provided with the source code for a similarity scoring tool at `/home/user/src/seq_cov.c`.
1. Compile this C code into an executable located at `/home/user/bin/seq_cov`. It requires the math library (`-lm`).
2. Make sure the executable has run permissions.

**Phase 2: Sequence Processing & Similarity Matrix**
Your dataset is located at `/home/user/data/seqs.txt`. It contains exactly one DNA sequence per line.
1. Run your compiled `seq_cov` executable, passing the path `/home/user/data/seqs.txt` as its only argument.
2. The program will output a symmetric, positive-definite covariance matrix (space-separated) to standard output.
3. Save this exact output to `/home/user/output/cov.txt`.

**Phase 3: Matrix Decomposition**
To decorrelate the features for your ML model, you need the lower triangular matrix $L$ from the Cholesky decomposition $A = LL^T$ of the covariance matrix.
1. Write an AWK script at `/home/user/scripts/cholesky.awk` that reads a space-separated square matrix from standard input and computes its Cholesky decomposition.
2. The script must output the lower triangular matrix $L$ (with zeros in the upper triangle).
3. Format each element to exactly 4 decimal places (e.g., `printf "%.4f"`) separated by a single space.
4. Run your script on `/home/user/output/cov.txt` and save the output to `/home/user/output/L_matrix.txt`.

**Phase 4: Feature Extraction via Numerical Integration**
You must compute a pseudo-energy integral feature for each sequence in `/home/user/data/seqs.txt`.
1. Create a Bash script at `/home/user/scripts/integrate.sh`.
2. The script should read `seqs.txt` line by line.
3. For each sequence, map the characters to numerical "energy" values: `A=1`, `C=2`, `G=3`, `T=4`.
4. Treat these values as equidistant points sampled at interval $\Delta x = 1.0$.
5. Compute the definite integral over the length of the sequence using the **Trapezoidal Rule**.
6. Output the integral for each sequence, one per line, formatted to exactly 1 decimal place.
7. Save the final list of integrals to `/home/user/output/integrals.txt`.

Ensure all directories (`/home/user/bin`, `/home/user/output`, `/home/user/scripts`) exist and are populated with exactly the filenames requested.