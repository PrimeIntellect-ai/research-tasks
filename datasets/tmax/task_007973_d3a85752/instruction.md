You are a bioinformatics analyst modeling the binding and 1D diffusion of a transcription factor (TF) along DNA sequences. 

You have a FASTA file at `/home/user/input.fasta` containing 5 DNA sequences, each exactly 50 base pairs long.

Your task is to:
1. Write a C++ program (`/home/user/simulate.cpp`) that simulates the concentration of the TF along each sequence over time using a 1D Reaction-Diffusion PDE. 
2. Use a 2D array (or equivalent multi-dimensional structure) to store and update the concentrations for all 5 sequences simultaneously.
3. Output the final concentrations at the end of the simulation to a CSV file `/home/user/output.csv` (5 rows, 50 columns, comma-separated, 4 decimal places).
4. Create a Jupyter Notebook (`/home/user/analyze.ipynb`) using Python that reads `output.csv`, identifies the maximum concentration value across the entire 2D space, and writes this single value to `/home/user/max_concentration.log` in the exact format: `Max Concentration: X.XXXX` (rounded to 4 decimal places). You must execute this notebook so the log file is generated.

**Mathematical Model:**
The concentration $u_i$ at base pair index $i$ (where $0 \le i < 50$) updates according to the explicit finite difference equation:
$u_i^{t+1} = u_i^t + \Delta t \left[ \frac{D}{(\Delta x)^2} (u_{i-1}^t - 2u_i^t + u_{i+1}^t) - k_{off} u_i^t + k_{on} S_i \right]$

Where:
* Initial condition: $u_i^0 = 0.0$ for all sequences and positions.
* Boundary conditions: Dirichlet boundaries where the ends are permanently zero. Thus, $u_0^t = 0.0$ and $u_{49}^t = 0.0$ at all times. The PDE only updates internal nodes $1 \le i \le 48$.
* $S_i$ is the sequence-dependent binding affinity at position $i$. Map the nucleotides to affinities as follows: 'A' = 1.0, 'T' = 0.8, 'C' = 0.5, 'G' = 0.2.
* Parameters: $D = 0.5$, $\Delta x = 1.0$, $\Delta t = 0.1$, $k_{off} = 0.01$, $k_{on} = 0.05$.
* Time steps: Run the simulation for exactly $N = 100$ time steps.

**Requirements:**
- Do not use external C++ libraries beyond the standard library.
- Compile your C++ program to `/home/user/simulate` and run it to produce the CSV.
- Ensure the Jupyter Notebook is fully reproducible and executed in the terminal (e.g., using `jupyter nbconvert --execute --inplace analyze.ipynb` or similar command-line runner).