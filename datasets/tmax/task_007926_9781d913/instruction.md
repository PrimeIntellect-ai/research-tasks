You are a bioinformatics analyst working on a pipeline for processing mass spectrometry data. Part of your reproducible computation pipeline relies on a Bash script that calculates the total energy of an idealized spectral peak (modeled as $f(x) = \exp(-x^2/2)$ from $x=-5$ to $x=5$) using adaptive numerical integration (Riemann sums).

The script is located at `/home/user/calc_energy.sh`.

It uses an iterative convergence algorithm: it calculates the integral with $N$ steps, compares the result to the previous iteration, and attempts to adapt the step size (by modifying $N$) based on the error. The pipeline is supposed to stop when the difference falls below $0.0001$. 

However, the numerical integrator diverges and crashes due to a flawed step-size adaptation logic. The variable $N$ incorrectly collapses to $0$, causing a division-by-zero error on the next iteration.

Your task:
1. Identify the mathematical or logical flaw in the step-size adaptation block of `/home/user/calc_energy.sh`.
2. Fix the Bash script so that it properly increases $N$ when the error is large (for example, using a correct error-ratio formula or a simple doubling strategy) and successfully converges.
3. Run the script. If successful, it will automatically write a line starting with `Converged: ` followed by the value to `/home/user/energy.log`.

Do not change the initial bounds, the target function, or the convergence threshold ($0.0001$).