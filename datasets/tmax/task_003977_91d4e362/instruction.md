You are an assistant helping a researcher verify a stochastic mesh-free method for solving a 1D boundary value problem (ODE/PDE). 

The problem is the 1D Laplace equation $u''(x) = 0$ on the domain $x \in [0, 100]$, with Dirichlet boundary conditions $u(0) = 10$ and $u(100) = 50$. We want to estimate $u(30)$ using a Monte Carlo random walk simulation.

Please write, compile, and execute a C program that estimates this value. 
Save your source code to `/home/user/mc_bvp.c`.

Requirements for the C program:
1. Perform $N = 100,000$ independent random walk trials.
2. Each trial must start at $x = 30$.
3. At each step of a trial, the walker moves left ($-1$) or right ($+1$). The trial ends when the walker hits either $x = 0$ or $x = 100$.
4. If it hits $0$, the score for that trial is $10$. If it hits $100$, the score is $50$.
5. To ensure strict reproducibility across environments, **do not** use the standard `rand()` function. Instead, implement the following specific Linear Congruential Generator (LCG):
   - Maintain a single global/static `unsigned long int state = 42;`
   - For every single step of the random walk, update the state: `state = (1103515245 * state + 12345) & 0x7FFFFFFF;`
   - Extract the step direction: `int bit = (state / 65536) % 2;`
   - If `bit == 0`, step left ($-1$). If `bit == 1`, step right ($+1$).
6. Keep a running sum of the scores of all $100,000$ trials.
7. Compute the average score as a `double`.
8. Write this exact average, formatted to exactly 4 decimal places (e.g., `22.1234`), to the file `/home/user/mc_pde_result.txt`.

Compile your code using `gcc -O3 /home/user/mc_bvp.c -o /home/user/mc_bvp` and run it to produce the output file.