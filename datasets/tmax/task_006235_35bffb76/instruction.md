You are a bioinformatics analyst tasked with processing a large set of DNA sequences stored in an HDF5 file. Your goal is to filter the sequences based on a specific primer, and calculate the overall GC content of the matched sequences using a parallel computing approach. 

Here are the requirements:
1. The sequences are stored in an HDF5 file located at `/home/user/data/seqs.h5` in a dataset named `sequences`.
2. Find all sequences that contain the exact primer sequence: `ATGCGATC`.
3. You must process the sequences in parallel (using multiple threads or processes) to speed up the computation. You can use any programming language of your choice.
4. To avoid non-reproducible results due to floating-point reduction order during parallel aggregation, you must aggregate the exact integer counts of G and C bases, as well as the total length of all matching sequences, before performing any floating-point division.
5. Compute the `average_gc_ratio` as the total number of G and C bases in all matching sequences divided by the total number of bases in all matching sequences.
6. Write your final statistics to a JSON file at `/home/user/results.json` with exactly the following keys:
   - `matched_count` (integer): The number of sequences containing the primer.
   - `total_gc` (integer): The total number of 'G' and 'C' bases across all matched sequences.
   - `total_bases` (integer): The total length (number of bases) of all matched sequences.
   - `average_gc_ratio` (float): The ratio of `total_gc` to `total_bases`, rounded to 6 decimal places.

Make sure your code cleanly handles the HDF5 file and parallelizes the search and counting efficiently. Write your script, execute it, and ensure `/home/user/results.json` is generated correctly.