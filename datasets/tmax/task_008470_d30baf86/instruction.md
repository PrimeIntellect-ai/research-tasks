You are a performance engineer optimizing a computational biology pipeline. We have a Python script `/home/user/profiler_test/process.py` that processes a FASTA file (`/home/user/profiler_test/reads.fasta`). 

For each sequence, the script:
1. Parses the FASTA file.
2. Computes the moving average of the GC content over a sliding window of size 100 (treating the sequence as a signal).
3. Finds the maximum GC moving average for the sequence.
4. Uses this maximum value as the decay constant `k` in a numerical ODE simulation ($dC/dt = -k \cdot C$, with $C(0) = 100$) integrated from $t=0$ to $t=10$.
5. Records the final concentration at $t=10$.

The current implementation is extremely slow because the moving average of the GC content is implemented with naive Python `for` loops.

Your task:
1. Analyze and profile the code in `/home/user/profiler_test/process.py`.
2. Write an optimized version of the script to `/home/user/profiler_test/process_optimized.py`. You must replace the slow sliding window GC calculation with an efficient, vectorized signal processing approach (e.g., using `numpy.convolve` or similar). 
3. Run your optimized script to generate the output file `/home/user/profiler_test/final_concentrations.csv`.

The output CSV must have exactly the same format and values (rounded to 5 decimal places) as the original script would produce, but your optimized script must be capable of processing the data much faster. The CSV header should be `SeqID,Final_C`.