I am a researcher studying chaotic systems, and I'm currently running a Monte Carlo simulation of a perturbed logistic map. However, my results have been non-reproducible across different machines due to floating-point reduction order and varying implementations of pseudo-random number generators in standard libraries. 

To fix this, I need you to create a strictly reproducible Bash-wrapper script that computes the simulation using standard tools (like `awk`) with a precise custom Linear Congruential Generator (LCG) for the Monte Carlo noise. 

I left a schematic image with the specific system parameters for the simulation in `/app/system_params.png`. You will need to extract the parameters from this image. It contains:
- `R` (the logistic map growth rate)
- `X0` (the initial state)
- `LCG_A`, `LCG_C`, `LCG_M` (the LCG parameters for noise generation)

Please write an executable Bash script at `/home/user/simulate.sh` that takes exactly two arguments:
1. `N` (integer, number of iterations)
2. `seed` (integer, initial seed for the LCG)

For each iteration $i$ from 1 to $N$, calculate:
1. The new LCG state: $S_i = (LCG\_A \times S_{i-1} + LCG\_C) \pmod{LCG\_M}$ (where $S_0 = seed$)
2. The perturbation: $perturb = (S_i / LCG\_M - 0.5) \times 0.01$
3. The new state: $X_i = R \times X_{i-1} \times (1 - X_{i-1}) + perturb$ (where $X_0$ is the initial state from the image).

The script must print the state $X_i$ at each step on a new line, formatted to exactly 6 decimal places (e.g., `0.512345`). Do not print anything else.
We will rigorously test your script's output against a verified oracle across many inputs to ensure exact equivalence and perfect reproducibility. Make sure all arithmetic is done in standard double-precision floating point (which standard `awk` uses).