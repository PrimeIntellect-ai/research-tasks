You are a performance engineer working on modernizing our scientific computing stack. We have a legacy stripped binary located at `/app/logistic_sim` that simulates population dynamics using the logistic growth ODE:
dy/dt = r * y * (1 - y / K)

We need to replace this black-box executable with a reproducible, highly optimized Python script. However, the original source code is lost, and we do not know which numerical integration scheme (e.g., Forward Euler, RK2, RK4, etc.) the original author used. 

Your task is to:
1. Probe and analyze the `/app/logistic_sim` binary to deduce the exact numerical integration method it employs. 
2. Write a Python script at `/home/user/py_sim.py` that perfectly replicates the binary's behavior.

The binary takes exactly 5 command-line arguments in this order:
`y0` (initial population, float)
`r` (growth rate, float)
`K` (carrying capacity, float)
`dt` (time step size, float)
`n_steps` (number of integration steps, integer)

Example usage:
`/app/logistic_sim 2.5 0.8 50.0 0.1 100`

The binary outputs a single string: the final value of `y` after `n_steps`, rounded to exactly 6 decimal places.

Your Python script (`/home/user/py_sim.py`) must accept the same command-line arguments in the same order and print identical output to standard out. The automated test suite will run an extensive fuzzing equivalence test against your script and the original binary using thousands of random input combinations to ensure bit-exact output reproduction. Do not hardcode answers; you must implement the correct numerical solver.