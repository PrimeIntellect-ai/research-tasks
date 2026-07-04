A researcher left a simulation code in `/home/user/integrator.c` that implements an adaptive step-size numerical integrator for a 2D system. Unfortunately, the simulation is diverging because the step-size adaptation logic is inverted.

Your task is to:
1. Identify and fix the logic bug in the `step_update` function in `/home/user/integrator.c`. The new step size should decrease when the error is larger than the tolerance, using the standard Runge-Kutta step adjustment formula: `h_new = h_old * 0.9 * (tol / error)^0.2`. Currently, it incorrectly puts `error / tol` in the formula.
2. Compile the fixed C program into an executable named `/home/user/integrator` using `gcc -O2 -lm`.
3. Run the executable. It will generate a raw binary file `/home/user/output.bin` containing a sequence of `double` precision floating point pairs (x, y).
4. Read the final (x, y) pair written to `output.bin`.
5. Calculate the Euclidean distance of this final point from the origin: $\sqrt{x^2 + y^2}$.
6. Write this distance to `/home/user/final_distance.txt`, formatted to exactly 4 decimal places (e.g., `1.0345`).

Ensure you have fully corrected the step update formula before running the integration, otherwise the output values will overflow and be invalid.