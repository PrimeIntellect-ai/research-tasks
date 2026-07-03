I am running a 1D heat equation simulation in C, but I'm encountering numerical instability. 

The source code is located at `/home/user/sim.c`. The simulation uses the Explicit Euler method, but the current number of time steps `N` is set to 100, which makes the time step `dt` too large and violates the von Neumann stability condition (CFL condition) for the 1D heat equation. 

Your task is to:
1. Analyze the parameters in `/home/user/sim.c` (domain size, spatial steps, diffusion coefficient `alpha`).
2. Calculate the minimum integer number of time steps `N` required to strictly satisfy the stability condition $\frac{\alpha \Delta t}{\Delta x^2} \le 0.5$.
3. Modify `/home/user/sim.c` to use this minimum stable integer value for `N`.
4. Compile the simulation using `gcc` (e.g., `gcc -O2 /home/user/sim.c -o /home/user/sim`).
5. Run the compiled executable. It will print the sum of the final temperature array.
6. Save this exact printed output to `/home/user/result.txt`.

Do not change any other mathematical logic, array indexing, or reduction order in the file, as it will affect the final floating-point sum. Only change the initialization of `N`.