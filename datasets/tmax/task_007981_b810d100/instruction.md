You are a performance engineer working on a bioinformatics pipeline. We have a numerical ODE solver written in Bash/Awk that models the folding decay of proteins. It uses a simple explicit Euler integration scheme.

However, the solver has a step-size adaptation bug: for stiff equations (which occur when the protein sequence is long), large time steps (`dt`) cause the integration to diverge and output "DIVERGED" instead of "STABLE".

You have been provided with:
1. `/home/user/proteins.fasta`: A FASTA file containing several protein sequences.
2. `/home/user/bin/simulate_ode.sh`: An ODE integrator script. It takes two arguments: the length of the protein sequence (an integer), and the time step `dt` (a float). 
   Example usage: `/home/user/bin/simulate_ode.sh 50 0.01`

Your task is to write a reproducible computational pipeline script at `/home/user/find_stable.sh` that does the following when executed:
1. Parses `/home/user/proteins.fasta` to determine the ID and sequence length (in characters) of each protein.
2. For each protein, tests the following `dt` values in descending order: `0.1`, `0.05`, `0.02`, `0.01`, `0.005`, `0.002`.
3. Finds the **largest** `dt` from that list that results in a "STABLE" output from `simulate_ode.sh`.
4. Outputs the results to a CSV file at `/home/user/results/stability.csv` with the format `SequenceID,MaxStableDt`. (Do not include a header row, just the data).

Requirements:
- Only use standard Bash built-ins, `awk`, `sed`, `grep`, or coreutils. Do not use Python, Perl, or other scripting languages.
- Ensure the output directory exists before writing to it.
- Your script must be executable and runnable without arguments.