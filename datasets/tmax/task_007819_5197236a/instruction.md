You are a data scientist fitting physical models to protein structures.

You have been given a C++ program at `/home/user/fit_plane.cpp` and a PDB structure file at `/home/user/structure.pdb`. 

The C++ program is designed to:
1. Parse the PDB file to extract the 3D coordinates of all C-alpha (`CA`) atoms.
2. Perform a simple spatial domain decomposition by splitting the atoms into two domains:
   - Domain 1: All atoms with an X-coordinate < 0
   - Domain 2: All atoms with an X-coordinate >= 0
3. Fit a local 2D plane to the points in each domain to model the surface. The plane equation is `z = ax + by + c`. It does this by solving the Ordinary Least Squares normal equations `(X^T X) W = X^T Z` using a custom 3x3 matrix inversion function.

**The Problem:**
The code currently prints `NaN` for the parameters of Domain 2. This is because the atoms in Domain 2 happen to be highly co-linear, forming a near-singular design matrix `X^T X`, which causes the matrix inversion to fail (division by zero determinant).

**Your Task:**
1. Fix the `fit_plane.cpp` program to prevent this failure by implementing Ridge Regression (Tikhonov regularization). Specifically, add an L2 penalty term by adding `1.0` (i.e., $\lambda = 1.0$) to the diagonal elements of the `X^T X` matrix *before* computing its inverse.
2. Compile your modified code. You can use `g++ -O2 /home/user/fit_plane.cpp -o /home/user/fit_plane`.
3. Run the compiled executable and save its standard output to exactly `/home/user/results.txt`.

The output format written by the fixed script should look like this:
```
Domain 1: a=..., b=..., c=...
Domain 2: a=..., b=..., c=...
```
*(Keep the output precision and formatting exactly as the original C++ program specifies, just ensure the NaNs are replaced by the correctly regularized fitted values).*