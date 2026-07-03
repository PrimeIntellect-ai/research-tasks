You are a performance engineer profiling a new matrix optimization pipeline. The pipeline currently reads extracted scientific data dumps, runs a gradient descent optimization script (`run_optim.sh`), and outputs the results. However, the optimization script frequently crashes with floating-point exceptions because it cannot handle near-singular matrices (matrices with a determinant very close to zero).

Your task is to write a purely Bash-based solution (using standard CLI tools like `awk`, `bc`, `grep`, etc.) to filter out these numerically unstable inputs before they reach the optimizer.

The extracted matrix data dumps are located in `/home/user/profiling/dumps/`. 
Each file (e.g., `mat_1.txt`) contains exactly two lines representing a 2x2 matrix, with space-separated floating-point numbers:
```text
a b
c d
```

You need to:
1. Iterate over all `.txt` files in `/home/user/profiling/dumps/`.
2. Parse the four values ($a, b, c, d$).
3. Calculate the determinant: $D = (a \times d) - (b \times c)$.
4. Determine if the matrix is "near-singular". We define this as the absolute value of the determinant being less than `0.01` ($|D| < 0.01$).
5. If the matrix is near-singular, append **only the filename** (e.g., `mat_2.txt`) to `/home/user/profiling/unstable.log`.
6. If the matrix is stable ($|D| \ge 0.01$), execute `/home/user/profiling/run_optim.sh` passing the **full path** of the file as the first argument. Append the standard output of this script to `/home/user/profiling/optim_results.log`.

Constraints:
- You must use Bash and standard POSIX/Linux utilities (e.g., `awk`, `bc`, loops). Do not write Python, Perl, or Ruby scripts.
- Make sure to sort `unstable.log` alphabetically at the end to ensure deterministic verification (e.g., `sort -o /home/user/profiling/unstable.log /home/user/profiling/unstable.log`).
- The files are located in `/home/user/profiling/dumps/`.