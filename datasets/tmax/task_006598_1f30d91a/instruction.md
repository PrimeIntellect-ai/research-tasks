You are a machine learning engineer tasked with preparing a C-based data processing pipeline. We are deploying a lightweight dimensionality reduction model (a pre-trained linear projection) on an edge device, and we need to process raw sensor data and verify the statistical properties of the projected embeddings.

You have two input files in your home directory:
1. `/home/user/X.csv`: A dataset of 100 samples and 10 features (100 rows, 10 columns, comma-separated floating-point numbers).
2. `/home/user/W.csv`: A pre-trained projection matrix for dimensionality reduction (10 rows, 3 columns).

Your task is to write a reproducible pipeline that performs model inference (matrix multiplication), dimensionality reduction, and statistical analysis in C.

Step 1: Write a C program (`/home/user/process.c`)
The program must:
1. Read `X.csv` and `W.csv` into double-precision arrays.
2. Use the OpenBLAS library (specifically `cblas_dgemm`) to compute the projected embeddings $Y = XW$. This reduces the dimensionality from 10 to 3.
3. Save the resulting 100x3 matrix to `/home/user/Y.csv`. Format the output with exactly 4 decimal places (e.g., `%.4f`), separated by commas.
4. Compute the 95% Confidence Interval (CI) for the sample mean of the *first* feature (column 0) of the projected matrix $Y$. 
   - Use the normal approximation formula: $\text{CI} = \bar{y} \pm 1.96 \times \frac{s}{\sqrt{N}}$
   - Where $\bar{y}$ is the sample mean, $s$ is the sample standard deviation (using $N-1$ in the denominator), and $N=100$.
5. Save this Confidence Interval to `/home/user/ci.txt` in exactly this format:
   `Lower: [val], Upper: [val]` (replace `[val]` with the numbers formatted to 4 decimal places).

Step 2: Write a Bash script (`/home/user/pipeline.sh`)
The script must:
1. Install any necessary dependencies for compiling and linking OpenBLAS (assume a Debian/Ubuntu-like environment using `apt-get` with `sudo`, e.g., `sudo apt-get update && sudo apt-get install -y libopenblas-dev`). (Note: use `sudo` for apt commands as needed, passwordless sudo is enabled).
2. Compile `process.c` into an executable named `process`, linking against OpenBLAS.
3. Run the compiled `process` executable.

Ensure your pipeline works end-to-end when `bash /home/user/pipeline.sh` is executed.