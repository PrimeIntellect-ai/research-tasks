As a computational biologist, I need to quickly extract spatial data from a protein structure and use it to seed an artificial diffusion simulation. 

Please write a C program that performs the following steps:
1. **Parse a Bioinformatics Format**: Read the PDB file located at `/home/user/protein.pdb`. Find the first three Alpha-Carbon atoms (identified by the exact string `CA` in the atom name field, which is the 3rd space-separated column in this specific file). 
2. **Extract Coordinates**: Extract the X, Y, and Z coordinates (which are the 6th, 7th, and 8th space-separated columns respectively) for these 3 atoms.
3. **Matrix Construction & Decomposition**: Construct a 3x3 matrix $A$, where the $i$-th row contains the X, Y, Z coordinates of the $i$-th CA atom. Perform an LU decomposition on $A$ (without partial pivoting, assuming Doolittle algorithm where the lower triangular matrix $L$ has 1s on the diagonal).
4. **ODE Numerical Solving**: Treat the resulting lower triangular matrix $L$ as the coefficient matrix in the linear ordinary differential equation system $\frac{d\vec{y}}{dt} = L \vec{y}$. Using the Forward Euler method, perform exactly **one** time step of size $\Delta t = 0.1$ starting from the initial condition $\vec{y}(0) = [1, 1, 1]^T$.

Write your C code to a file, compile it, and run it. Your C program must write the final 3 components of $\vec{y}(0.1)$ to a single line in `/home/user/result.txt`, separated by spaces, and formatted to exactly four decimal places (e.g., `1.0000 2.5000 3.1234`). 

You can use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.). No external numerical libraries (like LAPACK or GSL) are allowed.