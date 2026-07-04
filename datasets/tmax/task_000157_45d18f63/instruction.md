You are acting as a research assistant for a computational chemistry lab. The lab is trying to run a simplified 1D numerical simulation of a bond relaxing to an equilibrium distance. However, the simulation code is failing.

You have been provided with two files in your home directory (`/home/user`):
1. `molecule.pdb`: A standard PDB format file containing a diatomic molecule.
2. `simulate.cpp`: A C++ program written to simulate the nonlinear differential equation $dx/dt = -(x - 2.0)^3$, where $x$ is the bond distance over time $t$. 

Currently, the code has three major issues you must resolve:
1. The initial condition $x(0)$ is hardcoded to `0.0` in `simulate.cpp`. You must parse `molecule.pdb` to extract the 3D coordinates of the first two atoms (ATOM 1 and ATOM 2), calculate the Euclidean distance between them, and update `simulate.cpp` to use this distance as the initial value `x` in the `main` function.
2. The numerical integrator (an adaptive Euler method) is diverging and producing wild results or `NaN`. The researcher suspects that the step-size adaptation logic in the `adaptive_euler_step` function is reversed—it is increasing the step size `dt` when the local truncation error is too high, and decreasing it when the error is low. Fix this logic so it correctly halves `dt` when the error exceeds `tol`, and increases `dt` by a factor of 1.5 when the error is below `tol`.
3. The researcher wants automated validation against the analytical solution. The analytical solution for the distance at $t=10.0$, given $x(0) = 5.0$, is roughly $2.222987$. You must write a bash script at `/home/user/validate.sh` that:
   - Reads the final value printed by the compiled simulation.
   - Computes the analytical solution (or hardcodes the pre-calculated expected value for $x(0) = \text{your calculated distance}$).
   - Compares the simulation output to the analytical solution.
   - Exits with code `0` if the absolute difference is less than `0.005`, and exits with code `1` otherwise.

Your tasks:
1. Identify the initial distance from `molecule.pdb`.
2. Fix the bugs in `/home/user/simulate.cpp` (both the initial distance and the step-size adaptation).
3. Compile the program using `g++` and run it. Save the standard output of the run to `/home/user/result.txt`. The output should be a single floating-point number representing the distance at $t = 10.0$.
4. Create the executable bash script `/home/user/validate.sh` as described above. Run it to ensure it exits with code 0.

Ensure all file paths strictly follow `/home/user/...`.