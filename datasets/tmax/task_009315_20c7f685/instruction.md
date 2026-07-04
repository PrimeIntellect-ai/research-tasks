You are an AI assistant helping a scientific researcher with a numerical simulation pipeline. 

The researcher is studying a damped harmonic oscillator and needs to upgrade their numerical integration code. Their previous Euler method was numerically unstable and failed the regression tests. They need you to write a new solver in C using the 4th-order Runge-Kutta (RK4) method.

Here are the details of the task:

1. Create a directory `/home/user/sim` if it doesn't already exist.
2. Inside this directory, write a C program named `solver.c` that solves the following system of Ordinary Differential Equations (ODEs) using the 4th-order Runge-Kutta method:
   * Equation 1: dx/dt = v
   * Equation 2: dv/dt = -0.2*v - x
3. The simulation must use the following parameters:
   * Initial conditions: x(0) = 1.0, v(0) = 0.0
   * Start time: t = 0.0
   * End time: t = 10.0
   * Time step size: dt = 0.1
4. Compile the C program to an executable named `run_sim` using `gcc` (you may link the math library if needed).
5. Run the executable. It must compute the integration and write exactly one line containing the final state at t=10.0 to a file named `/home/user/sim/final_state.txt`. 
6. The format of the text in `/home/user/sim/final_state.txt` must be strictly as follows (formatted to exactly 5 decimal places):
   `t=10.00000, x=<value>, v=<value>`

Ensure your RK4 implementation is correct, as even small numerical errors will cause the implied regression test to fail. Do not output the entire time series to the file, only the final state.