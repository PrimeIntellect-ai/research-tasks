You are a performance engineer profiling a scientific application. In your workspace `/home/user/workspace/`, there is a data generation program written in C (`generate.c`) and an optimization script in Python (`optimize.py`).

The Python script uses Newton's method to solve a least-squares optimization problem by reading a matrix `A` and a vector `b` from an HDF5 file (`input.h5`), and it saves the optimized vector `x` to `solution.h5`. However, the script currently crashes due to `A` being a near-singular matrix, causing the Hessian inversion to fail.

Your tasks:
1. Compile the C program `generate.c` from source to an executable named `generate`. You must use the appropriate HDF5 C compiler wrapper available on the system.
2. Run the compiled executable to produce the `input.h5` data file.
3. Modify `optimize.py` to fix the singular matrix error by implementing **Tikhonov (L2) regularization** with a regularization parameter of `lambda = 1.0`. 
   - You must update the Hessian matrix (`H`) by adding the regularization term.
   - You must update the gradient vector (`grad`) by adding the corresponding regularization term.
4. Run the fixed `optimize.py` script so that it successfully completes and generates `solution.h5`.
5. Extract the first 3 elements of the dataset `x` from `solution.h5`, format them to 4 decimal places (e.g., `0.1234`), and save them space-separated on a single line to `/home/user/workspace/output.txt`.

Ensure your output in `output.txt` contains exactly the three formatted numbers.