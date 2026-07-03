You are an AI assistant helping a synthetic biology researcher run a coupled bioreactor simulation and design extraction primers. 

Your task requires managing a Python virtual environment, solving a system of Ordinary Differential Equations (ODEs), integrating the results, handling HDF5 scientific data, and performing basic sequence manipulation.

**Phase 1: Environment Setup**
Create a Python virtual environment at `/home/user/sim_env`. Install the necessary packages to perform ODE solving, numerical integration, HDF5 I/O, and sequence analysis (e.g., `numpy`, `scipy`, `h5py`, `biopython`). Ensure you use this environment for all subsequent steps.

**Phase 2: ODE Simulation**
We are simulating the temperature $T(t)$ and mRNA concentration $C(t)$ in a bioreactor from time $t=0$ to $t=50$ hours.
The system is governed by the following ODEs:
1. $dT/dt = -0.05 \cdot (T - 20)$
2. $dC/dt = 10 - 0.1 \cdot \exp\left(\frac{T - 20}{10}\right) \cdot C$

Initial conditions at $t=0$:
- $T(0) = 37.0$
- $C(0) = 0.0$

Solve this system using an appropriate ODE solver (e.g., `scipy.integrate.solve_ivp`) and evaluate the solution at exactly 500 evenly spaced time points between $t=0$ and $t=50$ (inclusive).
After solving, compute the definite integral of the concentration $C(t)$ over the entire time span $t \in [0, 50]$ using Simpson's rule (`scipy.integrate.simpson`).

**Phase 3: Scientific Data I/O**
Create a directory at `/home/user/results/`.
Save the simulated arrays `time`, `T`, and `C` into an HDF5 file located at `/home/user/results/simulation.h5`. Store them as datasets named `time`, `temperature`, and `concentration`.
Add an attribute to the root group (`/`) of the HDF5 file called `total_yield` containing the numerical value of the integral you computed.

**Phase 4: Primer Design**
An HDF5 file is already provided at `/home/user/data/reference.h5`. It contains a root-level dataset named `sequence` containing a string representing a 1000-bp reference genome.
Extract the target sequence from index 300 to exactly 500 (i.e., exactly 200 base pairs, where the start index is 300 and the end index is 499 in 0-based indexing).
Design the standard Forward and Reverse primers (each exactly 20 bases long) to amplify this 200-bp region:
- The Forward primer is the first 20 bases of the target region.
- The Reverse primer is the reverse complement of the last 20 bases of the target region.
Compute the GC content (percentage of G and C bases, from 0.0 to 100.0) for both primers.

**Phase 5: Output**
Create a JSON summary file at `/home/user/results/summary.json` containing exactly the following keys:
- `"integral_yield"`: The numerical value of the Simpson's rule integral of $C(t)$ (float, rounded to 2 decimal places).
- `"forward_primer"`: The string representation of the Forward primer (uppercase).
- `"reverse_primer"`: The string representation of the Reverse primer (uppercase).
- `"forward_gc"`: The GC content percentage of the Forward primer (float, rounded to 2 decimal places).
- `"reverse_gc"`: The GC content percentage of the Reverse primer (float, rounded to 2 decimal places).

Make sure all tasks are fully completed and the JSON file strictly conforms to these specifications.