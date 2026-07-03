You are a data scientist fitting a decay model to a set of genetic sequences. We are running a simple numerical integration script that simulates a stability profile over time for each sequence using the explicit Euler method to solve the ODE:
dy/dt = -k * y

Where:
- `y` is the sequence stability score (initial value y0 = 100).
- `k` is the decay constant, defined as the precise GC content ratio of the sequence (number of 'G' and 'C' bases divided by the total sequence length).
- The time step `dt` used in our legacy bash simulation script is fixed at exactly `2.5`.

Recently, we noticed that for certain sequences, the numerical integrator diverges wildly to infinity (oscillating) because the fixed step size `dt` violates the analytical stability criteria of the explicit Euler method for those specific `k` values.

Your task:
1. Parse the FASTA file located at `/home/user/sequences.fasta`.
2. Compute the decay constant `k` for each sequence.
3. Determine analytically which sequences will cause the explicit Euler integrator to strictly diverge (where the magnitude of the growth factor exceeds 1). 
4. Extract the IDs (the header line without the `>` character) of all diverging sequences.
5. Write these diverging sequence IDs to `/home/user/diverging.txt`, with one ID per line, sorted alphabetically.

You must accomplish this using only standard Bash shell tools (e.g., awk, grep, sed, etc.).