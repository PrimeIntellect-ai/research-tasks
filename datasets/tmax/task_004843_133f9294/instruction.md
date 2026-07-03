I am a researcher running a numerical simulation of diffusion on a 5-node ring network. I have a C program located at `/home/user/diffusion.c` that uses an adaptive step-size Euler method to integrate the ODE system. 

However, my integrator is diverging and eventually outputs `NaN` values. I suspect that the step-size adaptation logic is backwards—specifically, the line that calculates `dt_new`. Instead of shrinking the step size when the local truncation error is larger than the tolerance, it is growing it, causing the simulation to explode.

Please do the following:
1. Inspect `/home/user/diffusion.c` and locate the step-size adaptation calculation.
2. Fix the bug so that `dt_new` shrinks when `err > tol` and grows when `err < tol` (it should use the square root of the ratio, following standard adaptive Euler schemes).
3. Compile the fixed code using: `gcc -O3 /home/user/diffusion.c -lm -o /home/user/diffusion`
4. Run the simulation and save the standard output to `/home/user/final_state.txt`.

The final output file `/home/user/final_state.txt` should contain a single line of 5 space-separated floating-point numbers representing the final state of the network at $t = 2.0$.