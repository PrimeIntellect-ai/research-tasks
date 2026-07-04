You are acting as an AI assistant for a bioinformatics researcher. The researcher has run a sequence evolution simulation and saved the output in an HDF5 file. 

The file is located at `/home/user/sim_data.h5`. It contains a single dataset at the root level named `seqs`, which holds an array of simulated DNA sequences (stored as byte strings).

Your task is to write and execute a Python script (`/home/user/analyze.py`) that performs the following analysis:
1. Load the `seqs` dataset from the HDF5 file.
2. Separate the sequences into two groups based on a simple primer alignment: 
   - **Group A**: Sequences that contain the exact primer motif `GATTACA`.
   - **Group B**: Sequences that DO NOT contain the primer motif `GATTACA`.
3. For every sequence in both groups, calculate its GC content (the fraction of characters that are either 'G' or 'C'). For example, the GC content of "GCTAA" is 0.4.
4. Perform a statistical hypothesis comparison to determine if there is a significant difference in the mean GC content between Group A and Group B. Use Welch's t-test (an independent two-sample t-test that does not assume equal population variances).
5. Write the test results to a file named `/home/user/results.txt`. The file must contain exactly one line in this format:
   `T-statistic: [t_val], P-value: [p_val]`
   (Replace `[t_val]` and `[p_val]` with the calculated values rounded to 4 decimal places).

Assume a standard scientific Python environment (including `numpy`, `scipy`, and `h5py`) is available.