I need you to write a C program that models the geometry of a protein loop by fitting a 3D circle to the alpha-carbon (CA) atoms of a specific chain in a PDB (Protein Data Bank) file. 

Here is the full workflow:
1. **Environment**: You may need to install linear algebra packages (like `liblapacke-dev`) to perform matrix decompositions.
2. **PDB Parsing**: Write a C program at `/home/user/fit_loop.c` that accepts a PDB file path as its first command-line argument. It should parse the file and extract the X, Y, Z coordinates of all `CA` (Carbon Alpha) atoms belonging to Chain `A`.
3. **Plane Fitting**: The 3D points of the loop roughly lie on a plane. Find the best-fit plane using Principal Component Analysis (PCA) or Singular Value Decomposition (SVD). 
4. **Circle Fitting**: Project the 3D points onto this best-fit 2D plane. Then, perform a regression to fit a 2D circle to these projected points (you can use a linear least-squares algebraic circle fit).
5. **Output**: Your program must print the radius of the fitted circle to standard output in exactly this format: `Radius: <float>` (e.g., `Radius: 14.5291`).

To help you test your math, I have provided a compiled Linux binary at `/app/circle_fitter`. This stripped binary acts as an oracle: it takes a CSV file of X,Y,Z coordinates (no header, comma-separated) and computes the best-fit circle radius using the exact algorithm we expect. You can use it to verify your matrix decomposition and curve-fitting implementation.

Requirements:
- Your source code must be at `/home/user/fit_loop.c`.
- Compile it to `/home/user/fit_loop` (ensure it compiles cleanly with your chosen math libraries).
- Do not use external libraries other than standard C libraries and standard BLAS/LAPACK(E).
- The calculated radius must be highly accurate (within 0.001 of the oracle's output).

Please set up the environment, write the code, and ensure it exactly matches the oracle's mathematical results.