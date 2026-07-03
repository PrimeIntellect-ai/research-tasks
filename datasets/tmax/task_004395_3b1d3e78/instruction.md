You are an AI assistant helping a computational chemistry researcher. 

The researcher has found an old scanned document containing the reaction rate constants for a specific chemical process, located at `/app/reaction_rates.png`. 

Your task is to:
1. Extract the three rate constants (`ALPHA`, `BETA`, and `GAMMA`) from the image `/app/reaction_rates.png`.
2. Write a Go program that simulates the chemical reaction over time using the Euler method.
3. The program must be compiled to an executable named `/home/user/sim_runner`.

The chemical reaction is described by the following differential equations for species X, Y, and Z:
dX/dt = -ALPHA * X + BETA * Y
dY/dt = ALPHA * X - (BETA + GAMMA) * Y
dZ/dt = GAMMA * Y

Simulation details:
- Use a time step `dt = 0.1`.
- Run exactly 100 iterations (steps) of the Euler method.
- The program should take exactly 3 command-line arguments representing the initial concentrations: `X0`, `Y0`, `Z0` (as floating-point numbers).
- The output of the program must be printed to standard output (stdout) as a single line containing the final concentrations of X, Y, and Z separated by spaces, formatted to exactly 6 decimal places (e.g., `1.234567 0.123456 0.000000`).

Requirements:
- Your final executable must be at `/home/user/sim_runner`.
- It must be completely deterministic and reproducible.
- Make sure to handle standard floating point arithmetic (use `float64` in Go).
- You can use standard Go libraries.

Please write the Go code, compile it, and ensure it functions correctly according to the provided mathematical model and the constants extracted from the image.