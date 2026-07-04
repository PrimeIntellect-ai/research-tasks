You are a performance engineer tasked with profiling and debugging a biophysics simulation pipeline that has recently started crashing. The pipeline integrates the activation state of a light-sensitive protein over time. 

The simulation script is located at `/home/user/simulate.py`. It performs three main tasks:
1. Parses a FASTA file (`/home/user/data/protein.fasta`) to determine the decay constant $C$. The constant $C$ should be exactly `length_of_first_sequence * 0.12`.
2. Reads raw spectroscopy data from `/home/user/data/signal.csv` (columns: `time`, `intensity`). It acts as the driving force $I(t)$.
3. Integrates the ODE $dy/dt = -C \cdot y + I(t)$ with initial condition $y(0)=0$ from $t=0$ to $t=5.0$, using a custom adaptive-step integrator.

Currently, the custom numerical integrator in `/home/user/simulate.py` diverges and crashes with an overflow error. This is because the step-size adaptation logic is incorrectly implemented (it increases the step size when the error is large, rather than decreasing it).

Your tasks are to:
1. Identify and fix the step-size adaptation bug in the `adaptive_heun_step` function within `/home/user/simulate.py`. The formula should adapt the step size inversely proportional to the error, using the standard exponent $0.5$ for a second-order method: $h_{new} = 0.9 \cdot h \cdot (\text{tol} / \text{err})^{0.5}$.
2. Fix any missing or incorrect FASTA parsing logic in the script so that $C$ is correctly calculated.
3. Run the simulation.
4. Save the final integrated value $y(5.0)$ to the file `/home/user/result.txt`, rounded to exactly 4 decimal places (e.g., `1.2345`).

The raw data and the script are already present on the system.