You are a bioinformatics analyst modeling a 2-gene regulatory network. The system's steady state is defined by a system of non-linear ordinary differential equations (ODEs), which you are solving numerically by finding the roots of the network's rate equations using the Newton-Raphson method.

The core C program has already been written and is located at `/home/user/find_steady_state.c`. However, it currently fails and outputs `NaN` (Not a Number) because the initial biological state provided makes the Jacobian matrix perfectly singular at the first iteration, causing a division by zero during the matrix inversion.

Your task is to:
1. Fix the matrix inversion failure in `/home/user/find_steady_state.c` by implementing Tikhonov-style regularization. Specifically, add a small regularization term `lambda = 1e-6` to the main diagonal elements (`J[0][0]` and `J[1][1]`) of the Jacobian matrix *before* calculating the determinant and inverting it.
2. Compile the fixed C code into an executable named `/home/user/solver` using `gcc` and the math library.
3. Run the compiled solver. The program prints the final converged `x` and `y` concentrations. Redirect or format this output into a CSV file at `/home/user/steady_state.csv` with exactly this format:
   ```
   x,y
   <value_of_x>,<value_of_y>
   ```
4. Write a bash script at `/home/user/validate.sh` that validates the numerical solution against the analytical approximation. The script must:
   - Read `/home/user/steady_state.csv`.
   - Extract the `x` and `y` values.
   - Calculate their sum using standard bash tools (e.g., `awk` or `bc`).
   - If the sum is strictly between `0.9` and `1.1`, print exactly `VALID` to standard output. Otherwise, print `INVALID`.
   - Make sure `/home/user/validate.sh` is executable.

Do not change the initial guesses or the system equations in the C code; only add the regularization to the Jacobian.