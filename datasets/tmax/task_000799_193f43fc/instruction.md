You are a bioinformatics analyst tasked with processing sequence data. We need to compute a custom stability metric for nucleotide sequences based on a linear system and a Monte Carlo simulation. 

We have provided a vendored C-extension Python package at `/app/vendored/seqstats-1.0`. This package provides a fast nucleotide counting function `seqstats.count_bases(sequence)` which returns a tuple `(A, C, G, T)`. However, the package currently fails to install due to a misconfiguration in its build files. 

Your tasks are:
1. Identify and fix the bug in `/app/vendored/seqstats-1.0/setup.py` preventing its installation, and install the package in the system Python environment.
2. Write a Python script at `/home/user/process_seq.py` that takes a single FASTA file path as a command-line argument.
3. The script must parse the first sequence in the FASTA file (ignoring the header).
4. Use `seqstats.count_bases` to get the counts of 'A', 'C', 'G', and 'T' (case-insensitive). Let these be $N_A$, $N_C$, $N_G$, $N_T$.
5. Set up and solve the following system of linear equations for variables $x, y, z, w$ using `numpy.linalg.solve`:
   $2x + y + z + w = N_A$
   $x + 2y + z + w = N_C$
   $x + y + 2z + w = N_G$
   $x + y + z + 2w = N_T$
6. Perform a Monte Carlo simulation to estimate a stability parameter:
   - Initialize Python's built-in random number generator with `random.seed(N_A + N_C + N_G + N_T)`.
   - Draw exactly 10,000 samples using `random.gauss(mu, sigma)`, where `mu = x` and `sigma = max(y, 1.0)`.
   - Calculate the empirical mean of these samples (sum / 10,000).
7. The script must print exactly one line to standard output in the following format (all floating point values rounded to 4 decimal places):
   `x: <x_val>, y: <y_val>, z: <z_val>, w: <w_val>, mc_mean: <mc_mean_val>`

Example output:
`x: 10.2000, y: -5.4000, z: 2.0000, w: 1.0000, mc_mean: 10.2134`

Ensure your script is executable and robust. Automated verifiers will run your script against multiple random FASTA files and expect bit-exact output equivalence to our reference implementation.