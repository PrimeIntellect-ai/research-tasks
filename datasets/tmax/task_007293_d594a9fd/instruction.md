You are a researcher working on dimensionality reduction for time-series spatial data. You need to build a self-contained, reproducible pipeline that generates a synthetic 2D scalar field over time, computes its dominant mode using Singular Value Decomposition (SVD), and orchestrates the findings into a markdown report.

Your task is to write a C program and a Bash orchestration script with the following strict requirements:

1. **C Program (`/home/user/svd_sim.c`)**:
   - Generate data for a 2D spatial grid of size 100x100 over 10 time steps.
   - For $x \in \{0, \dots, 99\}$, $y \in \{0, \dots, 99\}$, and $t \in \{0, \dots, 9\}$, the scalar field is defined as:
     $F(x, y, t) = \sin(\frac{\pi x}{100}) \cdot \cos(\frac{\pi y}{100}) \cdot e^{-0.1 t}$
   - Flatten the spatial dimensions so that each time step is a column in a matrix $M$. The resulting matrix $M$ should have dimensions $10000 \times 10$.
   - Implement the Power Iteration method from scratch in C to find the largest singular value $\sigma_1$ of the matrix $M$. (Hint: Perform Power Iteration on $M^T M$ which is $10 \times 10$ to find the first right singular vector $V_1$, then calculate $\sigma_1 = \|M V_1\|_2$). Start your iteration with a vector of all ones. Run it for exactly 50 iterations.
   - The C program must write the computed largest singular value to a file named `/home/user/singular_value.txt`, formatted to exactly four decimal places (e.g., `12.3456`).

2. **Orchestration Script (`/home/user/pipeline.sh`)**:
   - Write a bash script that compiles `svd_sim.c` using standard `gcc` (with `-lm` for the math library).
   - Executes the compiled program.
   - Dynamically generates a markdown file `/home/user/notebook.md` that represents your "notebook-based workflow".
   - The markdown file must contain the exact string: `The dominant singular value is: <VALUE>` where `<VALUE>` is the exact contents of `singular_value.txt`.
   - Ensure the bash script is executable.

You may only use standard C libraries (`stdio.h`, `stdlib.h`, `math.h`). Do not use any external mathematical libraries like GSL or LAPACK. Ensure your files are saved exactly at the specified paths.