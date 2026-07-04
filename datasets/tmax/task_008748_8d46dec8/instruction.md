You are a performance engineer profiling a molecular graph simulation pipeline. 

There is a C program located at `/home/user/energy_calc.c` that computes the total potential energy of a molecular network for a given structural parameter `x`. It reads a list of edges from `/home/user/graph.dat`. The core calculation involves numerical integration over each edge.

However, the application is producing non-reproducible results. If you run the compiled binary multiple times with the exact same input parameter, the floating-point output fluctuates slightly. This is due to a floating-point reduction order issue caused by an inefficient and non-associative OpenMP atomic directive in the integration loop.

Your task:
1. Fix the bug in `/home/user/energy_calc.c` so that the result is completely deterministic across multiple runs without removing the parallelization (i.e., you must still use OpenMP, but fix the reduction method).
2. Compile the fixed C program into an executable named `/home/user/energy_calc`. Use the flags: `gcc -O2 -fopenmp -lm energy_calc.c -o energy_calc`.
3. Write a Python script `/home/user/optimize.py` that uses an optimization routine (e.g., from `scipy.optimize`) to find the value of `x` in the bounded range `[0.0, 5.0]` that *minimizes* the total energy returned by `./energy_calc <x>`.
4. Save ONLY the optimal value of `x`, rounded to exactly 4 decimal places (e.g., `1.2345`), to the file `/home/user/optimal_x.txt`.

Ensure your C program fix scales correctly and is strictly deterministic.