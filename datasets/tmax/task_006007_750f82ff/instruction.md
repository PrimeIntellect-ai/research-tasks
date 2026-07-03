I am running a simulation optimization, but I am getting non-reproducible results. Every time I run my optimization, the solver takes a slightly different path and ends up with a slightly different minimum. I suspect this is due to floating-point reduction order issues in my OpenMP C code.

I have placed a C file at `/home/user/simulation/objective.c`. This file contains a function `double compute_cost(double x, double y)` that computes a cost landscape using OpenMP parallelization.

Please do the following:
1. **Fix the non-reproducibility**: Identify the floating-point precision issue in `/home/user/simulation/objective.c` causing the OpenMP reduction to be non-deterministic across different thread thread timings, and fix it. (Hint: look at the data types used for the reduction variable).
2. **Compile the code**: Compile `objective.c` into a shared library named `/home/user/simulation/libobjective.so`. Ensure it is compiled with OpenMP support, Position Independent Code (PIC), and as a shared library. Use `gcc`.
3. **Write the optimization script**: Write a Python script at `/home/user/simulation/optimize.py`. This script must:
    - Load `libobjective.so` using `ctypes`.
    - Set up the correct argument and return types for `compute_cost`.
    - Define a Python wrapper function `cost_func(coords)` where `coords` is an array `[x, y]`.
    - Use `scipy.optimize.minimize` with the `Nelder-Mead` method to minimize `cost_func`. Start the optimization at `x0 = [0.0, 0.0]`.
    - Extract the optimized `x` and `y` coordinates from the `OptimizeResult` object.
    - Write the final optimized coordinates to `/home/user/simulation/result.txt` as a single line: `x,y` (both values rounded to exactly 4 decimal places).

Do not change the mathematical logic in the C file, only fix the data type of the accumulator to stabilize the reduction.