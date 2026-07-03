You are acting as a machine learning engineer who needs to establish spatial boundaries for a synthetic training dataset based on an estimated probability density curve. 

You have been provided with 3 critical sample points from this curve, which is known to be perfectly parabolic (degree-2 polynomial: $y = ax^2 + bx + c$). You need to find the specific $x$ boundaries where the density $y$ drops exactly to `0.5`.

To do this, you must write a C program that utilizes a custom, uncompiled linear algebra library provided on your system.

Here are your instructions:
1. Navigate to `/home/user/math_utils`. You will find the source code for a small C library (`system_solver.c` and `system_solver.h`) that solves 3x3 systems of linear equations.
2. Compile this source code into a shared library named `libsystemsolver.so` in the `/home/user/math_utils` directory.
3. The 3 sample points are located in `/home/user/data/density_points.csv`. Format: `x,y`.
4. Write a C program named `/home/user/src/compute_boundaries.c`. This program must:
   - Read the points from the CSV.
   - Formulate the 3x3 linear system required to find the coefficients ($a, b, c$) of the parabola passing through these points.
   - Dynamically link against `libsystemsolver.so` and use its `solve_3x3` function to find the coefficients.
   - Solve for the roots of the parabola where $y = 0.5$.
5. Compile your program to `/home/user/bin/compute_boundaries`. 
6. Run your program. It should write the two resulting $x$ boundary values to `/home/user/results/boundaries.txt`.
   - The file should contain a single line with the two values separated by a comma.
   - The smaller $x$ value must come first.
   - Format the floats to exactly 6 decimal places (e.g., `-1.234567,1.234567`).

Ensure all standard compiler flags are used for linking the shared library (e.g., `-L`, `-l`, and setting `LD_LIBRARY_PATH` when running).