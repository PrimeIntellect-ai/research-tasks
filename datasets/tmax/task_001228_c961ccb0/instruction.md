You are a bioinformatics analyst working on a new tool to predict DNA sequence conformation energies. 

We have a Monte Carlo simulation script located at `/home/user/mc_energy.py`. It calculates the conformational "binding energy" of a DNA sequence by generating 1000 random structural conformations as multi-dimensional arrays, evaluating them, and summing the energies. 

However, we are facing a critical issue: the simulation produces non-reproducible results. Every time we run `compute_energy("ACGTACGTACGTACGTACGT")`, the resulting floating-point number is slightly different. This is due to floating-point reduction order issues—the script uses a thread pool and accumulates results as they complete, leading to precision drift depending on thread execution order.

Your tasks:
1. **Fix the non-reproducibility**: Modify `/home/user/mc_energy.py`. Keep the `eval_conf` logic and the random seed generation exactly the same, but fix the reduction step. You must ensure the energies are evaluated and summed in their original generated order (index 0 to 999) and use `math.fsum` to avoid precision loss. After your fix, `compute_energy` must return the exact same float every time for a given sequence.

2. **Reshape Observational Data**: We have a raw data file at `/home/user/data/raw_reads.txt`. It contains a single continuous string of 100 nucleotides. Read this file and reshape it into exactly 5 distinct sequences of length 20.

3. **Optimization (Discrete)**: Create a script `/home/user/optimize.py`. For each of the 5 sequences, evaluate its initial energy. Then, evaluate the energy of *all possible single-point mutations* (changing exactly one nucleotide to A, C, G, or T, ensuring you don't mutate a base to itself). Find the specific single-point mutation that *minimizes* the energy. If there is a tie for the minimum energy, choose the mutated sequence that is alphabetically first.

4. **Output**: Your script `/home/user/optimize.py` must write the final results to `/home/user/results.csv`. The CSV must have a header row and exactly 5 data rows (one for each sequence from the raw file, in their original order).
The columns must be exactly: `original_sequence,original_energy,best_mutated_sequence,best_energy`.
Energies should be formatted to 6 decimal places.

Ensure you do not require root/sudo for any operations. Make sure your Python scripts use standard libraries or `numpy` (which is already installed).