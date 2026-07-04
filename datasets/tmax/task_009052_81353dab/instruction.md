You are acting as a research assistant for a computational physics lab. We are simulating a radioactive decay process described by the ordinary differential equation (ODE):
$dy/dt = -2y$
with the initial condition $y(0) = 1$. The analytical solution to this equation is known to be $y(t) = e^{-2t}$.

A previous lab member wrote a Bash/Awk script to numerically integrate this ODE using an adaptive step-size Euler method. The script is located at `/home/user/sim/integrate.sh`. It is supposed to integrate the system from $t=0$ to $t=2.0$.

However, the script has a critical bug in its step-size adaptation logic. Instead of reducing the step size when the local error is large, it incorrectly increases it, causing the simulation to rapidly diverge and output garbage values.

Your task:
1. Identify and fix the step-size adaptation bug in `/home/user/sim/integrate.sh`. (Hint: look at how `dt_new` is calculated relative to `err` and `tol`).
2. Write a validation script at `/home/user/sim/validate.sh` (must be executable) that does the following:
   a. Runs `./integrate.sh 2.0` and captures the output.
   b. Computes the Root Mean Square Error (RMSE) between the numerical solution (the $y$ values produced by the script) and the analytical solution $y(t) = e^{-2t}$ at the corresponding $t$ steps.
   c. Outputs the calculated RMSE to `/home/user/sim/rmse.log` in the exact format: `RMSE: X.XXXX` (rounded to 4 decimal places).
   d. Performs a statistical validation: if the RMSE is strictly less than `0.05`, write the string `PASS` to `/home/user/sim/status.log`. Otherwise, write `FAIL`.

Both `bc` and `awk` are available on your system to perform the necessary mathematical operations. Ensure all your paths are absolute and correct.