You are a performance engineer evaluating a new numerical simulation tool. You have been given a C++ program at `/home/user/stencil.cpp` that calculates the numerical Laplacian of a 2D function $f(x,y) = \sin(\pi x) \sin(\pi y)$ using a standard 5-point finite difference stencil on a grid of size $N \times N$. It compares the numerical result to the analytical solution and prints the maximum absolute error.

However, a recent regression test showed that the error does not converge to zero at the expected $O(h^2)$ rate as the grid is refined. 

Your tasks are:
1. Identify and fix the bug in the stencil calculation or multi-dimensional array manipulation in `/home/user/stencil.cpp`.
2. Compile the fixed C++ code. You can output the binary to `/home/user/stencil`.
3. Perform a convergence test by running the program for grid sizes $N = 10, 20, 40, \text{ and } 80$.
4. Save the maximum error outputs (exactly as printed by the program, one per line, in order of increasing $N$) to `/home/user/errors.txt`.

Do not change the formatting of the output in the C++ code; only fix the mathematical logic of the stencil.