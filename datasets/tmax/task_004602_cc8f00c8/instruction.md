You are assisting a researcher who is organizing datasets of high-dimensional sensor readings. The researcher uses a custom Bash pipeline to perform dimensionality reduction (via matrix projection) and validate model outputs by finding the nearest neighbor to a query point. 

However, they are facing a severe reproducibility issue: their projection outputs are heavily quantized or evaluating to zero, producing useless "blank" downstream plots (similar to a misconfigured rendering backend). The researcher suspects the issue lies in their vendored mathematical tool.

Your task has two parts:

**Part 1: Fix the Vendored Package**
The pipeline relies on GNU `bc` for precision math, whose source is vendored at `/app/bc-1.07.1`. A recent deliberate perturbation by a previous admin hardcoded the global `scale` initialization to `0` inside the C source code, ruining floating-point divisions and multiplications.
1. Find the perturbation in `/app/bc-1.07.1/bc/main.c` (or similar initialization file) where the default scale is forced to 0.
2. Change this default scale initialization to `20`.
3. Compile the package and install the resulting `bc` binary to `/home/user/bin/bc`. Ensure `/home/user/bin` is in your PATH.

**Part 2: Build the Dimensionality Reduction Pipeline**
Create a Bash script at `/home/user/process_embeddings.sh`. The script must accept exactly three arguments:
1. `DATASET_FILE`: Path to a CSV file where each line is an N-dimensional vector of floats (e.g., `0.5,1.2,-0.3`).
2. `PROJECTION_MATRIX`: Path to a CSV file representing an N x M projection matrix.
3. `QUERY_VECTOR`: A comma-separated string representing a single N-dimensional query vector.

Your script must:
1. Use your newly compiled `/home/user/bin/bc` and core coreutils/awk to multiply every vector in the `DATASET_FILE` by the `PROJECTION_MATRIX` to produce M-dimensional projected vectors.
2. Project the `QUERY_VECTOR` using the same matrix.
3. Calculate the Manhattan (L1) distance between each projected dataset vector and the projected query vector.
4. Print ONLY the 0-based line index of the dataset vector that is closest to the query vector. If there is a tie, print the lowest index.

Ensure your script handles errors gracefully and uses ONLY Bash built-ins, standard coreutils (like `awk`, `sed`, `paste`), and your compiled `bc`. No Python, Perl, or other interpreters may be used for the math.

Your script must be bit-exact equivalent in behavior to the researcher's reference implementation when given identically sized matrices and vectors.