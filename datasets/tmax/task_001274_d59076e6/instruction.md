You are a Machine Learning Engineer preparing 3D structural data for a neural network. You are dealing with atomic coordinates from Protein Data Bank (PDB) files, but some of your input structures represent near-planar or collinear molecules (near-singular inputs). Standard matrix factorization approaches to find the principal plane of these molecules fail due to singularity. 

To bypass this and extract spatial features robustly, you must implement a Regularized Gradient Descent algorithm in C to fit a plane to the atomic coordinates.

Your task:
1. Write a C program at `/home/user/fit_plane.c` that accepts exactly four command-line arguments:
   `./fit_plane <pdb_file_path> <learning_rate> <iterations> <lambda>`

2. The program must parse the provided PDB file. 
   - It should read line by line.
   - It should only process lines that begin with exactly `"ATOM  "` or `"HETATM"`.
   - From these lines, extract the X, Y, and Z coordinates. In standard PDB format, these are right-justified floats located at 1-based columns 31-38 (X), 39-46 (Y), and 47-54 (Z).

3. Implement Gradient Descent to fit a regression plane: $Z = w_1 X + w_2 Y + b$.
   The objective is to minimize the L2-regularized Mean Squared Error (Ridge Regression):
   $J(w_1, w_2, b) = \frac{1}{2m} \sum_{i=1}^m (Z_i - (w_1 X_i + w_2 Y_i + b))^2 + \frac{\lambda}{2} (w_1^2 + w_2^2)$
   where $m$ is the number of atoms parsed.
   
   Initialize weights: $w_1 = 0.0, w_2 = 0.0, b = 0.0$.
   At each iteration, compute the gradients exactly as:
   $dw_1 = \frac{1}{m} \sum_{i=1}^m ( \text{pred}_i - Z_i ) X_i + \lambda w_1$
   $dw_2 = \frac{1}{m} \sum_{i=1}^m ( \text{pred}_i - Z_i ) Y_i + \lambda w_2$
   $db = \frac{1}{m} \sum_{i=1}^m ( \text{pred}_i - Z_i )$
   where $\text{pred}_i = w_1 X_i + w_2 Y_i + b$.
   
   Update rule (simultaneous update):
   $w_1 = w_1 - \text{learning\_rate} \times dw_1$
   $w_2 = w_2 - \text{learning\_rate} \times dw_2$
   $b = b - \text{learning\_rate} \times db$

4. The program must print the final weights to standard output in exactly this format:
   `w1: <value>, w2: <value>, b: <value>`
   where `<value>` is formatted to exactly 4 decimal places (e.g., `%.4f`).

5. Write a Bash script `/home/user/process_data.sh` that:
   - Compiles `/home/user/fit_plane.c` into an executable named `/home/user/fit_plane` using `gcc` with `-O2 -lm`.
   - Runs the executable on all `.pdb` files located in `/home/user/pdb_data/` (process them in alphabetical order).
   - Uses `learning_rate = 0.01`, `iterations = 1000`, and `lambda = 0.5`.
   - Appends the output for each file into `/home/user/results.txt` in the format:
     `<filename>: w1: <val>, w2: <val>, b: <val>`
     (e.g., `mol1.pdb: w1: 0.1234, w2: 0.5678, b: 1.0000`)

Ensure you create `/home/user/process_data.sh` and make it executable, then run it to generate `/home/user/results.txt`. The directory `/home/user/pdb_data/` and its contents already exist.