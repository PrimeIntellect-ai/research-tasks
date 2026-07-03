You are a performance engineer tasked with accelerating a mathematical profiling suite. We need to compute the roots of a non-linear integral equation for a parameter sweep, and we need it done efficiently using parallel computation.

Your objective is to write, compile, and execute a C program that uses OpenMP to parallelize the root-finding process.

**Mathematical Problem:**
For a set of target values $C_i \in \{0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8\}$, find the corresponding $x_i$ such that:
$$ \int_0^{x_i} e^{-t^2} dt = C_i $$

**Algorithm Requirements:**
1.  **Root Finding:** Use the Newton-Raphson method. 
    *   Let $F(x) = \int_0^x e^{-t^2} dt - C_i$.
    *   The derivative is analytically known: $F'(x) = e^{-x^2}$.
    *   Use an initial guess of $x = 1.0$ for all $C_i$.
    *   Stop when $|F(x)| < 10^{-7}$ or after 100 iterations.
2.  **Numerical Integration:** To evaluate $F(x)$, you must numerically compute the integral $\int_0^x e^{-t^2} dt$ using the **Composite Simpson's 1/3 rule** with $N = 1000$ intervals (which means 1001 evaluation points from $0$ to $x$).
3.  **Parallelization:** Use OpenMP to parallelize the parameter sweep. The loop that iterates over the array of $C_i$ values must be parallelized using `#pragma omp parallel for`.

**System & Output Constraints:**
1.  Write your C code to `/home/user/root_finder.c`.
2.  Your C code must include `<omp.h>` and `<math.h>`.
3.  Write a bash script at `/home/user/build_and_run.sh` that compiles the C program with `gcc`, enabling OpenMP (`-fopenmp`), math libraries (`-lm`), and level 3 optimizations (`-O3`). The script must then execute the compiled binary.
4.  The compiled program must output the results to a CSV file located at `/home/user/roots.csv`. 
5.  The CSV file must have exactly one line per $C_i$ value, ordered from $C_i = 0.1$ to $0.8$, in the format: `C_i,x_i`. Format both numbers to exactly 6 decimal places (e.g., `0.100000,0.100335`).

Execute your bash script to ensure the binary is compiled and the output file is generated successfully.